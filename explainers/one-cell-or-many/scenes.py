"""One Cell, Many Jobs — a carried-world biology explainer.

COLOR MAP (shared by both films in this lesson)
  BLUE    movement
  GOLD    feeding
  TEAL    water balance
  GREEN   reproduction
  VIOLET  nerve signalling
  RED     oxygen carrying
  MAGENTA shared DNA
  ORANGE  tissues and organs

All cell pictures are schematic and not to scale.  The same builder functions are
used whenever a picture carries into the next scene, so landmarks do not drift.
"""
from bp_parts import *  # noqa: F401,F403


MOVE = BLUE
FEED = GOLD
WATER = TEAL
REPRO = GREEN
VIOLET = "#B58CD9"
MAGENTA = "#E06AA3"
ORANGE = "#F29E4C"


def arrow(a, b, color=TEXT, width=5, tip=0.22):
    return Arrow(a, b, buff=0.04, color=color, stroke_width=width,
                 tip_length=tip, max_tip_length_to_length_ratio=0.35)


def pond_field(opacity=0.32):
    """A moving-water backdrop, rebuilt identically for pond scenes."""
    lines = VGroup()
    for i, (x, y, length) in enumerate([
            (-5.8, 2.5, 2.0), (-2.4, 2.9, 1.5), (1.0, 2.5, 2.2), (4.2, 3.0, 1.6),
            (-6.1, -2.4, 1.7), (-3.0, -2.8, 2.2), (0.6, -2.5, 1.5), (3.5, -2.8, 2.1)]):
        ln = Line([x, y, 0], [x + length, y, 0], color=WATER, stroke_width=3,
                  stroke_opacity=opacity)
        ln.phase = i * 0.7
        base = ln.get_center().copy()
        def drift(m, dt, base=base):
            m.phase += 1.25 * dt
            m.move_to(base + RIGHT * 0.78 * np.sin(m.phase))
        ln.add_updater(drift)
        lines.add(ln)
    return lines


def paramecium(center=(0, 0, 0), width=8.0, height=3.6, stroke=TEXT,
                fill=TEAL, cilia=False, groove=False):
    """The carried Paramecium picture; every continuing scene calls this builder."""
    c = np.array(center, dtype=float)
    body = Ellipse(width=width, height=height, stroke_color=stroke, stroke_width=6,
                   fill_color=fill, fill_opacity=0.18).move_to(c)
    # A small offset inner line gives the slipper a directional, living outline.
    inner = Arc(radius=1, start_angle=-0.55, angle=1.12,
                color=stroke, stroke_width=3)
    inner.stretch_to_fit_width(width * 0.86).stretch_to_fit_height(height * 0.68)
    inner.set_fill(opacity=0).move_to(c + LEFT * 0.12)
    inner.set_opacity(0.42)
    g = VGroup(body, inner)
    g.body = body
    if groove:
        oral = Arc(radius=1, start_angle=-1.05, angle=2.1,
                   color=FEED, stroke_width=8)
        oral.stretch_to_fit_width(width * 0.34).stretch_to_fit_height(height * 0.72)
        oral.set_fill(opacity=0).move_to(c + LEFT * width * 0.12)
        g.add(oral)
        g.groove = oral
    if cilia:
        hairs = VGroup()
        for k, theta in enumerate(np.linspace(0, TAU, 42, endpoint=False)):
            p = c + np.array([width * 0.5 * np.cos(theta), height * 0.5 * np.sin(theta), 0])
            n = np.array([np.cos(theta) / width, np.sin(theta) / height, 0])
            n /= np.linalg.norm(n)
            tangent = np.array([-n[1], n[0], 0])
            hairs.add(Line(p, p + 0.28 * n + 0.08 * np.sin(k * 0.8) * tangent,
                           color=MOVE, stroke_width=3))
        g.add(hairs)
        g.cilia = hairs
    return g


def job_ring(word, color, radius=0.43, label=True):
    ring = Circle(radius=radius, color=color, stroke_width=7)
    if not label:
        return VGroup(ring)
    lab = T(word, 28, color, weight=BOLD).next_to(ring, DOWN, buff=0.12)
    return VGroup(ring, lab)


def four_jobs(scale=1.0):
    lb = scale >= 0.7
    jobs = VGroup(job_ring("move", MOVE, label=lb), job_ring("feed", FEED, label=lb),
                  job_ring("water", WATER, label=lb), job_ring("divide", REPRO, label=lb))
    jobs.arrange(RIGHT, buff=0.55 if lb else 0.33, aligned_edge=UP).scale(scale)
    return jobs


def traveling_cilia(hairs, speed=4.8, reach=0.16):
    """Keep the carried cilia beating as a visible wave, not a token pulse."""
    for i, hair in enumerate(hairs):
        start = hair.get_start().copy()
        end = hair.get_end().copy()
        tangent = np.array([-(end - start)[1], (end - start)[0], 0.0])
        tangent /= max(np.linalg.norm(tangent), 1e-6)
        hair.wave_t = i * 0.42
        def sway(m, dt, start=start, end=end, tangent=tangent):
            m.wave_t += speed * dt
            m.put_start_and_end_on(start, end + reach * np.sin(m.wave_t) * tangent)
        hair.add_updater(sway)
    return hairs


def inward_water_arrows(cell):
    c = cell.body.get_center()
    w, h = cell.body.width, cell.body.height
    specs = [
        (c + [-w * .34, h * .74, 0], c + [-w * .27, h * .43, 0]),
        (c + [0, h * .78, 0], c + [0, h * .45, 0]),
        (c + [w * .34, h * .74, 0], c + [w * .27, h * .43, 0]),
        (c + [-w * .56, -h * .22, 0], c + [-w * .47, -h * .17, 0]),
        (c + [w * .56, -h * .22, 0], c + [w * .47, -h * .17, 0]),
    ]
    return VGroup(*[arrow(a, b, WATER, 5, 0.18) for a, b in specs])


def predict_world():
    water = pond_field(0.24)
    cell = paramecium((0, 0.35, 0), 8.7, 3.5, stroke=TEXT)
    arrows = inward_water_arrows(cell)
    return VGroup(water, cell, arrows)


def star_vacuole(at, radius=0.42):
    star = Star(n=8, outer_radius=radius, inner_radius=radius * 0.52,
                stroke_color=WATER, stroke_width=6, fill_color=WATER, fill_opacity=0.22).move_to(at)
    channels = VGroup(*[Line(star.get_center() + 0.48 * radius * np.array([np.cos(a), np.sin(a), 0]),
                             star.get_center() + 1.8 * radius * np.array([np.cos(a), np.sin(a), 0]),
                             color=WATER, stroke_width=3) for a in np.linspace(0, TAU, 8, endpoint=False)])
    return VGroup(channels, star)


def daughter_pair():
    left = paramecium((-2.45, 0, 0), 4.25, 2.45, stroke=TEXT)
    right = paramecium((2.45, 0, 0), 4.25, 2.45, stroke=TEXT)
    return VGroup(left, right)


def muscle_cells(rows=2, cols=5, at=(0, 0, 0), scale=1.0):
    cells = VGroup(*[
        RoundedRectangle(corner_radius=0.18, width=1.25, height=0.52,
                         stroke_color=ORANGE, stroke_width=4,
                         fill_color=ORANGE, fill_opacity=0.16)
        for _ in range(rows * cols)])
    cells.arrange_in_grid(rows, cols, buff=(0.16, 0.18)).scale(scale).move_to(at)
    return cells


def tissue_sheet(at=(0, 0, 0), scale=1.0):
    return muscle_cells(3, 5, at, scale)


def heart(at=(0, 0, 0), scale=1.0, color=ORANGE):
    # A simple paired-lobe icon, intentionally schematic rather than anatomical.
    a = Circle(radius=0.92, color=color, stroke_width=6,
               fill_color=color, fill_opacity=0.17).shift(LEFT * 0.56)
    b = Circle(radius=0.92, color=color, stroke_width=6,
               fill_color=color, fill_opacity=0.17).shift(RIGHT * 0.56)
    tip = Polygon([-1.43, 0.12, 0], [1.43, 0.12, 0], [0, -1.65, 0],
                  color=color, stroke_width=6, fill_color=color, fill_opacity=0.17)
    return VGroup(a, b, tip).scale(scale).move_to(at)


def vessels(at=(0, 0, 0), scale=1.0):
    c = ORIGIN
    h = heart(c, 0.72)
    pipes = VGroup(
        Line(c + [-0.22, 0.65, 0], c + [-0.22, 2.0, 0], color=ORANGE, stroke_width=8),
        Line(c + [0.22, 0.65, 0], c + [0.22, 2.0, 0], color=ORANGE, stroke_width=8),
        ArcBetweenPoints(c + [-0.22, 2.0, 0], c + [-2.25, 0.1, 0], angle=1.0, color=ORANGE, stroke_width=7),
        ArcBetweenPoints(c + [0.22, 2.0, 0], c + [2.25, 0.1, 0], angle=-1.0, color=ORANGE, stroke_width=7),
        ArcBetweenPoints(c + [-2.25, 0.1, 0], c + [-0.65, -1.75, 0], angle=0.9, color=ORANGE, stroke_width=7),
        ArcBetweenPoints(c + [2.25, 0.1, 0], c + [0.65, -1.75, 0], angle=-0.9, color=ORANGE, stroke_width=7),
    )
    return VGroup(pipes, h).scale(scale).move_to(at)


class S00Title(TitleCard):
    LESSON = "One Cell or Many"
    TITLE = "One Cell, Many Jobs"

    def construct(self):
        field = pond_field(.25)
        field.remove(*list(field[:4]))
        cell = paramecium((0, -.45, 0), 7.7, 2.75, stroke=TEXT)
        title = T(self.TITLE, 50, TEXT, font=TITLE_FONT).move_to([0, 2.85, 0])
        lesson = T(self.LESSON.upper(), 28, TEAL).next_to(title, DOWN, buff=.18)
        rule = Line([-1.2, 1.9, 0], [1.2, 1.9, 0], color=GOLD, stroke_width=4)
        self.play(FadeIn(field), GrowFromCenter(cell), run_time=.75)
        self.play(Write(title), FadeIn(lesson), GrowFromCenter(rule), run_time=1.15)
        self.add(scope_tag("schematic • not to scale"))
        bob(cell, amp=.045, speed=1.3)
        self.finish()


class S01Hook(SpokenScene):
    def construct(self):
        drop = Circle(radius=0.34, color=WATER, stroke_width=6,
                      fill_color=WATER, fill_opacity=0.18)
        self.play(GrowFromCenter(drop), run_time=0.45)
        field = pond_field()
        self.play(Transform(drop, Circle(radius=6.5, color=WATER, stroke_opacity=0.18,
                                         fill_color=WATER, fill_opacity=0.035)),
                  FadeIn(field), run_time=0.8)
        self.at("one cell swim")
        cell = paramecium((-1.0, -0.25, 0), 7.7, 3.25, stroke=TEXT)
        bob(cell, amp=0.07, speed=1.4)
        self.play(GrowFromCenter(cell), run_time=0.85)
        q = fit_text("How can one cell do every job?", 10.5, 40, GOLD,
                     font=TITLE_FONT).move_to([0, 3.18, 0])
        self.play(FadeIn(q, shift=DOWN * 0.12), run_time=0.55)
        self.at("In pond water")
        jobs = four_jobs(0.82).move_to([1.4, -2.6, 0])
        self.play(LaggedStart(*[FadeIn(j, shift=LEFT * 0.15) for j in jobs], lag_ratio=0.17), run_time=1.35)
        self.at("Watch where")
        self.play(jobs.animate.shift(UP * 0.12), rate_func=there_and_back, run_time=0.9)
        self.finish()


class S02One(SpokenScene):
    def construct(self):
        cell = paramecium((0, -0.2, 0), 9.2, 4.2, stroke=TEXT)
        bob(cell, amp=0.045, speed=1.3)
        self.play(GrowFromCenter(cell), run_time=0.8)
        self.at("one cell")
        label = fit_text("unicellular: one cell, one organism", 10.8, 36, TEXT).move_to([0, 3.15, 0])
        self.play(FadeIn(label), cell.body.animate.set_stroke(GOLD, width=9), run_time=0.75)
        self.at("no tissues")
        tissue = tissue_sheet((-4.9, -2.65, 0), 0.55).set_opacity(0.36)
        organ = heart((4.75, -2.55, 0), 0.5).set_opacity(0.36)
        self.play(FadeIn(tissue), FadeIn(organ), run_time=0.5)
        self.at("Its whole life")
        self.play(tissue.animate.shift(LEFT * 2.2).set_opacity(0),
                  organ.animate.shift(RIGHT * 2.2).set_opacity(0),
                  Circumscribe(cell.body, color=GOLD, time_width=0.5), run_time=1.25)
        self.finish()


class S02bComplete(SpokenScene):
    def construct(self):
        para = paramecium((-4.2, 0.25, 0), 3.65, 2.0, stroke=TEXT)
        bacterium = RoundedRectangle(corner_radius=0.55, width=2.35, height=1.12,
                                     color=MOVE, stroke_width=6, fill_color=MOVE,
                                     fill_opacity=0.12).move_to([0, 0.25, 0])
        alga = Circle(radius=0.92, color=REPRO, stroke_width=6,
                      fill_color=REPRO, fill_opacity=0.12).move_to([3.85, 0.25, 0])
        self.play(FadeIn(para), run_time=0.45)
        self.at("Bacteria")
        self.play(GrowFromCenter(bacterium), run_time=0.55)
        self.at("many algae")
        self.play(GrowFromCenter(alga), run_time=0.55)
        names = VGroup(T("protist", 28, TEXT), T("bacterium", 28, MOVE), T("alga", 28, REPRO))
        for name, obj in zip(names, [para, bacterium, alga]):
            name.next_to(obj, DOWN, buff=0.24)
        self.play(FadeIn(names), run_time=0.6)
        self.at("complete organism")
        halos = VGroup(*[SurroundingRectangle(o, buff=0.22, corner_radius=0.18,
                                               color=GOLD, stroke_width=4) for o in [para, bacterium, alga]])
        self.play(Create(halos), run_time=0.8)
        self.at("not one cell")
        piece = VGroup(Rectangle(width=3.1, height=1.25, color=GREY, stroke_width=4),
                       T("piece of a body", 28, GREY)).move_to([0, -2.45, 0])
        piece[1].layout_ok = True  # Deliberate label inside the crossed-out example.
        cross = Cross(piece, stroke_color=RED, stroke_width=8)
        self.play(FadeIn(piece), Create(cross), run_time=0.85)
        self.finish()


class S03Move(SpokenScene):
    def construct(self):
        field = pond_field(0.28)
        cell = paramecium((0, 0.1, 0), 9.1, 4.0, stroke=TEXT, cilia=True)
        self.add(field, cell.body, cell[1])
        self.at("Short cilia")
        self.play(LaggedStart(*[GrowFromCenter(h) for h in cell.cilia], lag_ratio=0.018), run_time=1.0)
        self.at("beat together")
        wave = ValueTracker(0)
        self.play(wave.animate.set_value(TAU),
                  LaggedStart(*[Rotate(h, angle=0.34, about_point=h.get_start(), rate_func=there_and_back)
                                for h in cell.cilia], lag_ratio=0.018), run_time=1.8, rate_func=linear)
        self.at("pushing the cell")
        streaks = VGroup(*[Line([-5.8, y, 0], [-3.8, y, 0], color=MOVE, stroke_width=4,
                                     stroke_opacity=0.55) for y in [-1.25, -0.45, 0.55, 1.35]])
        self.play(streaks.animate.shift(LEFT * 1.2), cell.animate.shift(RIGHT * 0.55), run_time=1.4)
        self.at("Movement stays")
        ring = job_ring("move", MOVE).move_to([5.7, -2.65, 0])
        self.play(FadeIn(ring), ring.animate.move_to(cell.body.get_right() + LEFT * 2.4 + UP * 0.35), run_time=0.9)
        self.finish()


class S04Feed(SpokenScene):
    def construct(self):
        field = pond_field(0.24)
        cell = paramecium((0, 0.1, 0), 9.1, 4.0, stroke=TEXT, cilia=True, groove=True)
        traveling_cilia(cell.cilia)
        pulse(cell.body, base=6, amp=1.5, speed=2.2)
        self.add(field, cell)
        food = VGroup(*[Dot([-5.8 - i * .25, 1.35 - i * .22, 0], radius=0.12, color=FEED) for i in range(4)])
        self.at("Food such as bacteria")
        self.play(FadeIn(food), run_time=0.45)
        self.at("swept into a groove")
        self.play(food.animate.move_to(cell.groove.get_center() + LEFT * .1), run_time=1.25)
        self.at("food vacuole")
        vac = Circle(radius=0.47, color=FEED, stroke_width=6, fill_color=FEED,
                     fill_opacity=0.18).move_to(cell.groove.get_center())
        self.play(ReplacementTransform(food, vac), run_time=0.75)
        self.at("travels through")
        crumbs = VGroup(*[Dot(radius=r, color=FEED) for r in [0.1, 0.085, 0.07]]).arrange(RIGHT, buff=0.08).move_to(vac)
        self.play(vac.animate.move_to([2.6, -0.45, 0]),
                  crumbs.animate.move_to([2.6, -0.45, 0]), run_time=2.0, rate_func=smooth)
        self.at("Digestion also")
        pulse(vac)
        self.play(crumbs.animate.scale(0.62), run_time=0.8)
        self.finish()


class S04bBoundary(SpokenScene):
    def construct(self):
        field = pond_field(0.24)
        cell = paramecium((0, 0.1, 0), 9.1, 4.0, stroke=TEXT, cilia=True, groove=True)
        traveling_cilia(cell.cilia)
        pulse(cell.body, base=6, amp=1.5, speed=2.2)
        vac = Circle(radius=0.47, color=FEED, stroke_width=6, fill_color=FEED,
                     fill_opacity=0.18).move_to([2.6, -0.45, 0])
        self.add(field, cell, vac)
        boxes = VGroup(*[DashedVMobject(Rectangle(width=2.45, height=2.25, color=GREY,
                                                   stroke_width=3).move_to([x, 0.1, 0]))
                         for x in [-2.75, 0, 2.75]])
        self.at("separate organs")
        self.play(FadeIn(boxes), run_time=0.7)
        self.at("Moving feeding")
        rings = VGroup(job_ring("move", MOVE, .36), job_ring("feed", FEED, .36),
                       job_ring("digest", FEED, .36)).arrange(RIGHT, buff=.9, aligned_edge=UP).move_to([0, -2.45, 0])
        self.play(FadeIn(rings), run_time=0.75)
        self.at("within the membrane")
        self.play(FadeOut(boxes), cell.body.animate.set_stroke(GOLD, width=10),
                  rings.animate.shift(UP * 0.18), run_time=1.15)
        pulse(cell.body, base=8, amp=2, speed=2)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        world = predict_world()
        cell = world[1]
        self.add(world[0], cell)
        self.at("water keeps moving inward")
        self.play(LaggedStart(*[GrowArrow(a) for a in world[2]], lag_ratio=0.13),
                  cell.animate.scale(1.06), run_time=1.7)
        self.at("If that continued")
        q = question_card("Water keeps entering. What must the cell do?", y=-3.12, size=30)
        self.play(FadeIn(q.question), run_time=0.65)
        pulse(cell.body, base=6, amp=1.8, speed=2)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "Water keeps entering. What must the cell do?"
    SECONDS = 5.0
    CARD = {"y": -3.12, "size": 30}
    def backdrop(self):
        return predict_world()


class S07Water(SpokenScene):
    def construct(self):
        field = pond_field(0.22)
        cell = paramecium((0, 0.25, 0), 8.8, 3.55, stroke=TEXT)
        self.add(field, cell)
        self.at("remove the extra water")
        out = VGroup(arrow([-4.0, .35, 0], [-5.55, .35, 0], WATER, 6),
                     arrow([4.0, .35, 0], [5.55, .35, 0], WATER, 6))
        self.play(GrowArrow(out[0]), GrowArrow(out[1]), cell.animate.scale(.96), run_time=0.9)
        self.at("Two contractile vacuoles")
        left = star_vacuole((-3.05, .25, 0), .42)
        right = star_vacuole((3.05, .25, 0), .42)
        self.play(GrowFromCenter(left), GrowFromCenter(right), run_time=0.75)
        self.at("fill and squeeze")
        self.play(left.animate.scale(1.65), right.animate.scale(1.65), run_time=1.15)
        self.play(left.animate.scale(.35).set_opacity(.15), right.animate.scale(.35).set_opacity(.15),
                  out.animate.set_stroke(width=9), run_time=0.8)
        self.at("cycle repeats")
        self.play(left.animate.scale(3.0).set_opacity(1), right.animate.scale(3.0).set_opacity(1),
                  cell.animate.scale(1 / .96), run_time=1.4)
        self.finish()


class S08Divide(SpokenScene):
    def construct(self):
        cell = paramecium((0, 0.2, 0), 8.4, 3.5, stroke=TEXT)
        jobs = four_jobs(.78).move_to([0, 2.85, 0])
        self.add(cell)
        self.at("For reproduction")
        self.play(FadeIn(jobs), Rotate(jobs, angle=TAU / 10), run_time=0.9)
        self.at("copies what it needs")
        copies = jobs.copy().scale(.74).move_to(cell)
        self.play(TransformFromCopy(jobs, copies), run_time=0.85)
        self.at("pinches into two")
        daughters = daughter_pair().shift(DOWN * .1)
        self.play(ReplacementTransform(cell, daughters),
                  copies.animate.arrange_in_grid(2, 2, buff=.55), run_time=1.65)
        self.at("movement feeding")
        left_jobs = four_jobs(.46).move_to([-2.45, -2.55, 0])
        right_jobs = four_jobs(.46).move_to([2.45, -2.55, 0])
        self.play(ReplacementTransform(copies, VGroup(left_jobs, right_jobs)), run_time=1.0)
        self.finish()


class S08bFission(SpokenScene):
    def construct(self):
        pair = daughter_pair()
        label = T("binary fission", 38, REPRO, font=TITLE_FONT).move_to([0, 3.05, 0])
        self.at("Binary fission")
        self.play(FadeIn(label), FadeIn(pair), run_time=0.85)
        self.at("without a partner")
        empty = DashedVMobject(Circle(radius=.65, color=GREY, stroke_width=4)).move_to([0, -2.25, 0])
        partner = T("no partner", 28, GREY).next_to(empty, DOWN, buff=.16)
        self.play(FadeIn(empty), FadeIn(partner), run_time=.65)
        self.at("divides into two")
        self.play(pair[0].animate.shift(LEFT * .65), pair[1].animate.shift(RIGHT * .65),
                  FadeOut(empty), FadeOut(partner), run_time=1.1)
        self.at("each new cell")
        jobs_l = four_jobs(.43).move_to([-3.1, -2.4, 0])
        jobs_r = four_jobs(.43).move_to([3.1, -2.4, 0])
        self.play(LaggedStart(FadeIn(jobs_l), FadeIn(jobs_r), lag_ratio=.22), run_time=1.0)
        bob(pair[0], amp=.05, speed=1.4); bob(pair[1], amp=.05, speed=1.4, seed=2)
        self.finish()


class S09Many(SpokenScene):
    def construct(self):
        panels = TwoPanel("separate organisms", "one many-celled organism",
                          colors=(TEXT, ORANGE), top=3.25, bottom=-2.65, size=30)
        self.add(panels)
        pair = daughter_pair().scale(.52)
        panels.put(pair, "left")
        self.play(FadeIn(pair), run_time=.55)
        self.at("multicellular organism")
        body = RoundedRectangle(corner_radius=.8, width=5.0, height=3.65,
                                color=ORANGE, stroke_width=6, fill_color=ORANGE,
                                fill_opacity=.06)
        cells = VGroup(*[Circle(radius=.36, color=ORANGE, stroke_width=4,
                                fill_color=ORANGE, fill_opacity=.14) for _ in range(12)]).arrange_in_grid(3, 4, buff=.23)
        organism = VGroup(body, cells)
        panels.put(organism, "right")
        self.play(FadeIn(organism), run_time=.8)
        self.at("different cells")
        colors = [MOVE, FEED, WATER, REPRO]
        self.play(*[cells[i].animate.set_stroke(colors[i], width=6).set_fill(colors[i], .22)
                    for i in range(4)], run_time=.85)
        self.at("specialized")
        shapes = VGroup(Rectangle(width=1.2, height=.35, color=MOVE, stroke_width=5),
                        Circle(radius=.48, color=FEED, stroke_width=5),
                        Star(n=7, outer_radius=.55, inner_radius=.27, color=WATER, stroke_width=5),
                        RoundedRectangle(corner_radius=.1, width=.75, height=.75, color=REPRO, stroke_width=5))
        for s, old in zip(shapes, cells[:4]): s.move_to(old)
        self.play(*[ReplacementTransform(cells[i], shapes[i]) for i in range(4)], run_time=1.05)
        self.at("structure fits")
        self.play(LaggedStart(*[Indicate(s, color=s.get_color(), scale_factor=1.12) for s in shapes],
                              lag_ratio=.14), run_time=1.0)
        self.finish()


class S10Levels(SpokenScene):
    def construct(self):
        cells = muscle_cells(1, 5, (-3.65, 1.65, 0), .48)
        self.at("specialized cells")
        self.play(LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=.1), run_time=.85)
        self.at("as a tissue")
        tissue = tissue_sheet((3.4, 1.45, 0), .52)
        self.play(TransformFromCopy(cells, tissue), run_time=.95)
        tl = T("tissue", 28, ORANGE).next_to(tissue, UP, buff=.22)
        self.play(FadeIn(tl), run_time=.35)
        self.at("build an organ")
        organ = heart((-3.55, -1.2, 0), .92)
        self.play(TransformFromCopy(tissue, organ), run_time=1.0)
        ol = T("organ", 28, ORANGE).next_to(organ, DOWN, buff=.25)
        self.play(FadeIn(ol), run_time=.35)
        self.at("organ system")
        system = vessels((3.45, -1.0, 0), .84)
        self.play(TransformFromCopy(organ, system), run_time=1.0)
        sl = T("organ system", 28, ORANGE).next_to(system, DOWN, buff=.18)
        self.play(FadeIn(sl), run_time=.35)
        arrows = VGroup(*[arrow(a, b, ORANGE, 4, .16) for a, b in [
            (cells.get_right()+RIGHT*.12, tissue.get_left()+LEFT*.12),
            (tissue.get_bottom()+DOWN*.12, organ.get_top()+UP*.12),
            (organ.get_right()+RIGHT*.12, system.get_left()+LEFT*.12)]])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=.2), run_time=.8)
        self.finish()


class S10bExample(SpokenScene):
    def construct(self):
        head = T("a concrete example", 34, ORANGE, font=TITLE_FONT).move_to([0, 3.15, 0])
        self.add(head)
        cells = muscle_cells(1, 5, (-3.65, 1.45, 0), .48)
        self.at("Muscle cells")
        self.play(LaggedStart(*[GrowFromCenter(c) for c in cells], lag_ratio=.1), run_time=.8)
        self.at("muscle tissue")
        tissue = tissue_sheet((3.4, 1.35, 0), .52)
        self.play(TransformFromCopy(cells, tissue), run_time=.95)
        self.at("form the heart")
        organ = heart((-3.55, -1.25, 0), .92)
        self.play(TransformFromCopy(tissue, organ), run_time=1.0)
        self.at("blood vessels")
        system = vessels((3.45, -1.05, 0), .84)
        self.play(TransformFromCopy(organ, system), run_time=1.15)
        names = VGroup(T("cells", 28, ORANGE).next_to(cells, DOWN, buff=.28),
                       T("tissue", 28, ORANGE).next_to(tissue, UP, buff=.22),
                       T("heart", 28, ORANGE).next_to(organ, DOWN, buff=.28),
                       T("circulatory system", 28, ORANGE).next_to(system, DOWN, buff=.22))
        self.play(LaggedStart(*[FadeIn(n) for n in names], lag_ratio=.14), run_time=.75)
        self.finish()


class S11Limit(SpokenScene):
    def construct(self):
        cell = RoundedRectangle(corner_radius=.75, width=9.4, height=4.5,
                                color=ORANGE, stroke_width=7, fill_color=ORANGE,
                                fill_opacity=.09).move_to([0, -.15, 0])
        fibres = VGroup(*[Line([-3.5, y, 0], [3.5, y, 0], color=ORANGE,
                               stroke_width=9) for y in [-.9, -.25, .4]])
        self.play(GrowFromCenter(cell), FadeIn(fibres), run_time=.75)
        self.at("muscle cell")
        self.play(fibres.animate.stretch(.72, 0), run_time=.85)
        food = VGroup(*[Dot([-5.6, y, 0], radius=.12, color=FEED) for y in [-.7, 0, .7]])
        self.at("takes in food molecules")
        self.play(FadeIn(food), food.animate.shift(RIGHT * 2.0), run_time=1.15)
        self.at("makes a TP")
        energy = ValueTracker(.18)
        gauge = dial(energy, center=[3.25, 0.6, 0], radius=0.5, label="ATP energy",
                     color=GOLD, fmt="{:.0f}%", scale=100, size=34)
        self.play(FadeIn(gauge), energy.animate.set_value(.82), run_time=1.25)
        self.at("maintains itself")
        gap = Line([4.7, -.55, 0], [4.7, .55, 0], color=BG, stroke_width=12)
        repair = Line([4.7, -.55, 0], [4.7, .55, 0], color=ORANGE, stroke_width=8)
        self.play(FadeIn(gap), run_time=.35)
        self.play(Create(repair), run_time=.85)
        self.at("Specialized means")
        rule = caption("especially fitted for one job — not limited to one job", size=30, color=TEXT)
        self.play(FadeIn(rule), fibres.animate.stretch(1.2, 0), run_time=.95)
        self.finish()


class S12Close(SpokenScene):
    def construct(self):
        panels = TwoPanel("one cell", "many cells", colors=(TEAL, ORANGE),
                          top=3.2, bottom=-2.45, size=34)
        self.add(panels)
        para = paramecium((0, 0, 0), 4.8, 2.35, stroke=TEXT, cilia=True, groove=True)
        panels.put(para, "left")
        many = tissue_sheet((0, 0, 0), .82)
        panels.put(many, "right")
        self.at("Paramecium")
        self.play(FadeIn(para), run_time=.7)
        self.at("every life process")
        jobs = four_jobs(.48)
        jobs.move_to(panels.area("left")[0] + DOWN * 1.75)
        self.play(LaggedStart(*[FadeIn(j) for j in jobs], lag_ratio=.15), run_time=1.1)
        self.at("many celled organism")
        self.play(FadeIn(many), run_time=.7)
        self.at("share major jobs")
        tokens = VGroup(job_ring("move", MOVE, .3, False), job_ring("feed", FEED, .3, False),
                        job_ring("water", WATER, .3, False), job_ring("divide", REPRO, .3, False))
        tokens.arrange(RIGHT, buff=.22).scale(.82)
        tokens.move_to(panels.area("right")[0] + DOWN * 1.75)
        self.play(LaggedStart(*[TransformFromCopy(many[i], tokens[i]) for i in range(4)], lag_ratio=.16), run_time=1.25)
        self.at("shaped for their work")
        self.play(LaggedStart(*[Indicate(many[i], color=[MOVE, FEED, WATER, REPRO][i], scale_factor=1.18)
                                for i in range(4)], lag_ratio=.14), run_time=1.0)
        self.finish()


class S13End(EndCard):
    LINE = "One cell can do every life job, or many cells share them."
