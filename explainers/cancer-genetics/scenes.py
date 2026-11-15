"""One Cell, Two Routes.

COLOR MAP (fixed across both cancer-genetics chapters)
  GREY / TEXT = ordinary cells and DNA
  CLAY        = acquired somatic change and the selected lineage
  GOLD        = inherited / germline first hit
  BLUE        = active growth signal / oncogene accelerator
  GREEN       = working tumour-suppressor brake
  RED         = lost function
  TEAL        = sequencing reads (reserved for chapter 2)

All gene copies are labelled blocks or bars, never molecular structures.  The
cell, brake and retinal worlds are rebuilt by shared builders wherever carried.
"""
from bp_parts import *  # noqa: F401,F403


CLAY = "#C9825B"


def tissue_cell(at, radius=0.82, stroke=GREY, fill=0.32):
    """A schematic tissue cell; optional badges are added by the caller."""
    c = Circle(radius=radius, stroke_color=stroke, stroke_width=4,
               fill_color=stroke, fill_opacity=fill).move_to(at)
    n = Circle(radius=radius * 0.24, stroke_color=GREY, stroke_width=2,
               fill_color=GREY, fill_opacity=0.12).move_to(at)
    g = VGroup(c, n)
    g.body, g.nucleus = c, n
    return g


def badge(color=CLAY, radius=0.15):
    return Circle(radius=radius, stroke_width=0, fill_color=color, fill_opacity=1)


TISSUE_POS = [(-4.55, 1.05), (-2.15, 1.15), (0.25, 1.05),
              (-3.35, -1.15), (-0.95, -1.20), (1.45, -1.05)]


def six_cell_tissue(marked=False):
    cells = VGroup(*[tissue_cell([x, y, 0], 0.94) for x, y in TISSUE_POS])
    if marked:
        m = badge().move_to(cells[2].get_center() + RIGHT * 0.34)
        cells[2].add(m)
        cells[2].mark = m
    return cells


def family_cell(at, marked=False, passenger=False, radius=0.48):
    c = tissue_cell(at, radius, stroke=CLAY if marked else GREY,
                    fill=0.34 if marked else 0.28)
    if marked:
        c.add(badge(CLAY, radius * 0.16).move_to(c.get_center() + LEFT * radius * 0.27))
    if passenger:
        c.add(Dot(c.get_center() + RIGHT * radius * 0.27,
                  radius=radius * 0.09, color=TEXT))
    return c


def selection_tree(final=True, passenger=True):
    """Carried clay family tree used for selection and the closing rule."""
    root = family_cell([-5.2, 0, 0], True, False, 0.58)
    level1 = VGroup(family_cell([-2.65, 1.45, 0], True, passenger, 0.52),
                    family_cell([-2.65, -1.45, 0], False, False, 0.52))
    clay_pts = [(0.0, 2.35), (0.0, 0.85), (0.0, -0.5)]
    pale_pts = [(0.0, -2.25)]
    clay = VGroup(*[family_cell([x, y, 0], True, passenger, 0.46) for x, y in clay_pts])
    pale = VGroup(*[family_cell([x, y, 0], False, False, 0.46) for x, y in pale_pts])
    links1 = VGroup(Arrow(root.get_right(), level1[0].get_left(), buff=0.1,
                          color=CLAY, stroke_width=5, tip_length=0.2),
                    Arrow(root.get_right(), level1[1].get_left(), buff=0.1,
                          color=GREY, stroke_width=3, tip_length=0.2))
    links2 = VGroup(*[Arrow(level1[0].get_right(), c.get_left(), buff=0.1,
                                color=CLAY, stroke_width=6, tip_length=0.2) for c in clay],
                    Arrow(level1[1].get_right(), pale[0].get_left(), buff=0.1,
                          color=GREY, stroke_width=3, tip_length=0.2))
    g = VGroup(root, links1, level1, links2, clay, pale)
    g.root, g.links1, g.level1, g.links2, g.clay, g.pale = root, links1, level1, links2, clay, pale
    return g


def division_wheel(center=(2.45, 0.0, 0), radius=1.45):
    c = np.array(center, dtype=float)
    rim = Circle(radius=radius, color=TEXT, stroke_width=10).move_to(c)
    spokes = VGroup(*[Line(c, c + radius * 0.82 * np.array([np.cos(a), np.sin(a), 0]),
                            color=GREY, stroke_width=9) for a in np.linspace(0, TAU, 8, endpoint=False)])
    hub = Dot(c, radius=0.18, color=TEXT)
    wheel = VGroup(rim, spokes, hub)
    wheel.spin_speed = 0.16

    def turn(mob, dt):
        mob.rotate(mob.spin_speed * dt, about_point=c)
    wheel.add_updater(turn)
    return wheel


def brake_world(question=False):
    """Exact carried frame for the prediction, pause, and suppressor reveal."""
    cell = Circle(radius=3.0, color=GREY, stroke_width=4,
                  fill_color=GREY, fill_opacity=0.24).move_to([0, -0.15, 0])
    wheel = division_wheel((2.2, -0.15, 0), 1.28)
    lost = RoundedRectangle(width=0.34, height=2.45, corner_radius=0.08,
                            stroke_color=RED, fill_color=RED, fill_opacity=0.9).move_to([-1.25, -0.15, 0])
    crack = VGroup(Line([-1.45, 0.25, 0], [-1.07, -0.02, 0], color=BG, stroke_width=5),
                   Line([-1.07, -0.02, 0], [-1.42, -0.35, 0], color=BG, stroke_width=5))
    working = RoundedRectangle(width=0.42, height=2.8, corner_radius=0.08,
                               stroke_color=GREEN, fill_color=GREEN, fill_opacity=0.95).move_to([0.64, -0.15, 0])
    world = VGroup(cell, wheel, lost, crack, working)
    world.cell, world.wheel, world.lost, world.crack, world.working = cell, wheel, lost, crack, working
    return world


PREDICT_QUESTION = "Does the cell lose the brake now, or can one copy hold it?"


def retinal_cell(at, first_hit=True, second_hit=False, r=0.53):
    c = tissue_cell(at, r)
    if first_hit:
        c.add(badge(GOLD, r * 0.15).move_to(c.get_center() + LEFT * r * 0.28))
    bar_color = RED if second_hit else GREEN
    bar = RoundedRectangle(width=r * 0.18, height=r * 0.8, corner_radius=0.04,
                           stroke_width=0, fill_color=bar_color, fill_opacity=1)
    bar.move_to(c.get_center() + RIGHT * r * 0.27)
    c.add(bar)
    c.bar = bar
    return c


RETINA_POS = [(-4.4, 1.35), (-2.9, 1.65), (-1.35, 1.5), (0.25, 1.55), (1.85, 1.3),
              (-4.15, -0.25), (-2.55, 0.0), (-0.95, -0.15), (0.65, -0.05), (2.25, -0.35),
              (-3.45, -1.75), (-1.75, -1.6), (-0.05, -1.65), (1.55, -1.75)]


def retina_world(second_index=None):
    outline = Ellipse(width=9.0, height=5.4, stroke_color=GREY, stroke_width=4,
                      fill_color=GREY, fill_opacity=0.22).move_to([-1.0, -0.1, 0])
    cells = VGroup(*[retinal_cell([x, y, 0], True, i == second_index)
                     for i, (x, y) in enumerate(RETINA_POS)])
    g = VGroup(outline, cells)
    g.outline, g.cells = outline, cells
    return g


def route_panel_cells(inherited=True):
    pts = [(-1.4, 0.7), (0.0, 0.7), (1.4, 0.7), (-0.7, -0.8), (0.7, -0.8)]
    cells = VGroup(*[retinal_cell([x, y, 0], first_hit=inherited, r=0.42) for x, y in pts])
    if not inherited:
        for c in cells:
            # Pale lineages begin with two working copies represented by the unmarked cell + green bar.
            pass
        cells[3].add(badge(CLAY, 0.07).move_to(cells[3].get_center() + LEFT * 0.13))
        cells[3].bar.set_fill(RED, 1)
    else:
        cells[3].bar.set_fill(RED, 1)
    return cells


class S00Hook(SpokenScene):
    def construct(self):
        tissue = six_cell_tissue(False)
        question = fit_text("If cancer is genetic, why is it usually not inherited?",
                            max_w=11.2, size=36, color=GOLD).move_to([0, 3.25, 0])
        for i, c in enumerate(tissue):
            bob(c, amp=0.055, speed=1.2 + 0.08 * i, seed=i)
        self.play(FadeIn(tissue), FadeIn(question), run_time=0.8)
        self.at("Watch one pale tissue cell")
        mark = badge().move_to(tissue[2].get_center() + RIGHT * 0.34)
        self.play(FadeIn(mark, scale=0.4), run_time=0.7)
        self.at("That cell divides")
        tissue[2].clear_updaters()
        a = family_cell([0.0, 1.35, 0], True, False, 0.62)
        b = family_cell([1.55, 1.15, 0], True, False, 0.62)
        self.play(FadeOut(mark), ReplacementTransform(tissue[2], a),
                  TransformFromCopy(a, b), run_time=1.15)
        self.at("change follows its daughters")
        c = family_cell([0.1, 0.0, 0], True, False, 0.5)
        d = family_cell([1.4, -0.05, 0], True, False, 0.5)
        self.play(a.animate.scale(0.86), b.animate.scale(0.86),
                  TransformFromCopy(a, c), TransformFromCopy(b, d), run_time=1.2)
        for i, cell in enumerate((a, b, c, d)):
            bob(cell, amp=0.045, speed=1.1 + i * 0.12, seed=i)
        self.at("Nearby cells lack it")
        self.play(Indicate(VGroup(tissue[0], tissue[1], tissue[3], tissue[4], tissue[5]),
                           color=TEXT, scale_factor=1.03), run_time=0.8)
        self.at("This is a somatic change")
        label = boxed_label("somatic: acquired during life", CLAY, 30).move_to([3.25, -3.05, 0])
        self.play(FadeOut(question), FadeIn(label), run_time=0.7)
        self.at("not a change carried")
        self.play(Indicate(VGroup(a, b, c, d), color=CLAY, scale_factor=1.04), run_time=0.8)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Cancer genetics"
    TITLE = "One Cell, Two Routes"


class S02Selection(SpokenScene):
    def construct(self):
        tree = selection_tree(passenger=False)
        bob(tree.root, amp=0.13, speed=1.4)
        for i, c in enumerate(list(tree.level1) + list(tree.clay) + list(tree.pale)):
            bob(c, amp=0.085, speed=1.05 + 0.08 * i, seed=i + 1)
        self.play(FadeIn(tree.root), run_time=0.5)
        self.at("driver lets cells divide")
        self.play(Create(tree.links1), FadeIn(tree.level1), run_time=1.0)
        driver = boxed_label("driver", CLAY, 30).next_to(tree.level1[0], UP, buff=0.18)
        self.play(FadeIn(driver), run_time=0.45)
        self.at("Its branch widens")
        self.play(Create(tree.links2), FadeIn(tree.clay), FadeIn(tree.pale), run_time=1.4)
        self.at("A passenger may ride")
        p0 = Dot(tree.level1[0].get_center() + RIGHT * 0.15, radius=0.075, color=TEXT)
        pd = VGroup(*[Dot(c.get_center() + RIGHT * 0.14, radius=0.065, color=TEXT) for c in tree.clay])
        passenger = boxed_label("passenger", TEXT, 28).move_to([3.6, -2.65, 0])
        self.play(FadeIn(p0), FadeIn(passenger), run_time=0.55)
        self.at("did not cause the widening")
        self.play(*[TransformFromCopy(p0, q) for q in pd], run_time=1.0)
        self.at("Selection acts on cells")
        self.play(FadeOut(driver), FadeOut(passenger), Indicate(tree.clay, color=CLAY,
                                                               scale_factor=1.04), run_time=1.0)
        self.at("marks spread with them")
        self.play(Indicate(VGroup(tree.level1[0], tree.clay), color=CLAY,
                           scale_factor=1.035), run_time=0.9)
        self.finish()


class S03Oncogene(SpokenScene):
    def construct(self):
        cell = Circle(radius=2.85, color=GREY, stroke_width=4,
                      fill_color=GREY, fill_opacity=0.24).move_to([-0.8, -0.1, 0])
        bob(cell, amp=0.1, speed=1.35)
        self.play(FadeIn(cell), run_time=0.5)
        self.at("proto -duoncogene normally promotes growth")
        copies = VGroup(boxed_label("gene copy", TEXT, 29, box=(2.25, 0.72)),
                        boxed_label("gene copy", TEXT, 29, box=(2.25, 0.72))).arrange(DOWN, buff=0.72)
        copies.move_to([-1.35, 0.0, 0])
        bob(copies, amp=0.045, speed=1.15)
        self.play(FadeIn(copies[0]), FadeIn(copies[1]), run_time=0.8)
        self.at("gain of function change")
        track = RoundedRectangle(width=3.4, height=0.72, corner_radius=0.34,
                                 color=BLUE, stroke_width=4).move_to(copies[0])
        knob = Circle(radius=0.28, color=BLUE, fill_color=BLUE, fill_opacity=1).move_to(track.get_left() + RIGHT * 0.42)
        on = T("ON", 30, BLUE, weight=BOLD).next_to(track, RIGHT, buff=0.25)
        self.play(Succession(FadeOut(copies[0], run_time=0.2),
                             AnimationGroup(FadeIn(track), FadeIn(knob), run_time=0.35)))
        self.at("one switch locked on")
        self.play(knob.animate.move_to(track.get_right() + LEFT * 0.42), FadeIn(on), run_time=0.8)
        arrow = Arrow([2.1, -0.1, 0], [5.45, -0.1, 0], buff=0.0, color=BLUE,
                      stroke_width=10, tip_length=0.35)
        pulse(arrow, base=8, amp=2, speed=2.2)
        divide = T("division", 31, BLUE).next_to(arrow, UP, buff=0.24)
        self.at("One altered allele")
        self.play(FadeIn(arrow), FadeIn(divide), run_time=0.65)
        self.at("Extra gene copies")
        extras = VGroup(*[boxed_label("copy", BLUE, 25, box=(1.15, 0.55)) for _ in range(3)]).arrange(RIGHT, buff=0.2)
        extras.move_to([-1.2, -0.72, 0])
        self.play(Succession(FadeOut(copies[1], run_time=0.25),
                             FadeIn(extras, run_time=0.45)))
        self.at("translocation can also activate")
        rearranged = extras.copy().arrange(RIGHT, buff=0.45).rotate(0.08).move_to([-1.2, -0.72, 0])
        self.play(Transform(extras, rearranged), run_time=0.7)
        self.add(scope_tag("schematic"))
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        world = brake_world()
        self.play(FadeIn(world.cell), FadeIn(world.wheel), run_time=0.55)
        self.at("two tumor suppressor copies")
        green2 = world.working.copy().move_to([-1.25, -0.15, 0])
        self.play(FadeIn(green2), FadeIn(world.working), run_time=0.6)
        self.at("One turns red")
        self.play(Transform(green2, world.lost), FadeIn(world.crack), run_time=0.8)
        self.at("other remains green")
        self.play(Indicate(world.working, color=GREEN, scale_factor=1.04), run_time=0.55)
        self.at("Predict")
        q = question_card(PREDICT_QUESTION, y=3.3, size=31, max_w=11.0)
        self.play(FadeIn(q), run_time=0.65)
        self.at("working copy still hold it")
        world.wheel.spin_speed = 0.12
        self.play(world.wheel.animate.shift(LEFT * 0.16), rate_func=there_and_back, run_time=1.0)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = PREDICT_QUESTION
    SECONDS = 4.5
    CARD = {"y": 3.3, "size": 31, "max_w": 11.0}

    def backdrop(self):
        return brake_world()


class S06Suppressor(SpokenScene):
    def construct(self):
        world = brake_world()
        self.add(world)
        holds = boxed_label("one working copy holds", GREEN, 29).move_to([-3.9, 3.15, 0])
        usually = boxed_label("usually", GOLD, 25).move_to([-5.25, 1.95, 0])
        self.play(FadeIn(holds), FadeIn(usually), run_time=0.65)
        self.at("A second loss")
        crack2 = VGroup(Line([0.43, 0.28, 0], [0.84, -0.02, 0], color=BG, stroke_width=6),
                        Line([0.84, -0.02, 0], [0.46, -0.38, 0], color=BG, stroke_width=6))
        self.play(world.working.animate.set_fill(RED, 1).set_stroke(RED), FadeIn(crack2),
                  FadeOut(holds), run_time=0.8)
        self.at("growth or survival advantage")
        world.wheel.spin_speed = 0.85
        self.play(world.wheel.animate.shift(RIGHT * 0.65), run_time=1.0)
        self.at("branch may expand")
        tree = selection_tree(passenger=False).scale(0.7).move_to([0.4, -0.05, 0])
        for i, c in enumerate(list(tree.level1) + list(tree.clay) + list(tree.pale)):
            bob(c, amp=0.05, speed=1.0 + i * 0.1, seed=i)
        bob(tree.root, amp=0.12, speed=1.3)
        pulse(tree.links1, base=5, amp=2.5, speed=1.5)
        pulse(tree.links2, base=6, amp=3, speed=1.35)
        self.play(FadeOut(VGroup(world.cell, world.lost, world.crack, world.working, crack2)),
                  ReplacementTransform(world.wheel, tree), run_time=1.1)
        caution = boxed_label("can expand, not must", CLAY, 29).move_to([4.1, -2.55, 0])
        self.play(FadeIn(caution), run_time=0.5)
        self.at("does not by itself guarantee")
        self.play(Indicate(caution, color=GOLD, scale_factor=1.03), run_time=0.7)
        self.at("usually recessive within one cell")
        rule = caption("usually: both copies lose function", 30, RED)
        self.play(FadeOut(caution), FadeIn(rule), run_time=0.65)
        self.at("exceptions to these rules")
        self.play(Indicate(usually, color=GOLD, scale_factor=1.08), run_time=0.65)
        self.add(scope_tag("schematic"))
        self.finish()


class S07Inherited(SpokenScene):
    def construct(self):
        head = Circle(radius=0.6, color=GREY, stroke_width=4).move_to([0, 2.25, 0])
        body = RoundedRectangle(width=2.5, height=3.8, corner_radius=1.1,
                                color=GREY, stroke_width=4).move_to([0, -0.45, 0])
        body_cells = VGroup(*[retinal_cell([x, y, 0], True, r=0.32)
                              for x, y in [(-0.55, 0.55), (0.55, 0.55), (-0.55, -0.55),
                                           (0.55, -0.55), (0, -1.45)]])
        person = VGroup(head, body, body_cells)
        for i, c in enumerate(body_cells):
            bob(c, amp=0.04, speed=1.0 + i * 0.1, seed=i)
        bob(person, amp=0.11, speed=1.35)
        self.play(FadeIn(person), run_time=0.75)
        self.at("Gold first -hit badges")
        self.play(Indicate(body_cells, color=GOLD, scale_factor=1.04), run_time=0.7)
        self.at("including every retinal cell")
        retina = retina_world()
        label = T("retina", 34, TEXT).move_to([4.55, 2.35, 0])
        self.play(ReplacementTransform(person, retina), FadeIn(label), run_time=1.0)
        for i, c in enumerate(retina.cells):
            bob(c, amp=0.025, speed=1.0 + 0.03 * i, seed=i)
        self.at("raises risk")
        risk = boxed_label("risk rises", GOLD, 29).move_to([4.45, 0.6, 0])
        self.play(FadeIn(risk), run_time=0.55)
        self.at("does not make every cell")
        no_tumor = boxed_label("not a tumor", TEXT, 27).move_to([4.55, -3.15, 0])
        self.play(FadeIn(no_tumor), run_time=0.55)
        self.at("one working copy")
        self.play(Indicate(VGroup(*[c.bar for c in retina.cells]), color=GREEN,
                           scale_factor=1.04), run_time=0.9)
        self.at("pass to the next generation")
        arrow = Arrow([3.55, -1.65, 0], [5.55, -1.65, 0], color=GOLD,
                      stroke_width=6, tip_length=0.3)
        self.play(FadeOut(risk), FadeOut(no_tumor), GrowArrow(arrow), run_time=0.7)
        self.add(scope_tag("schematic"))
        self.finish()


class S08SecondHit(SpokenScene):
    def construct(self):
        retina = retina_world()
        for i, c in enumerate(retina.cells):
            bob(c, amp=0.03, speed=1.0 + i * 0.04, seed=i)
        bob(retina, amp=0.09, speed=1.25)
        self.add(retina, T("retina", 34, TEXT).move_to([4.55, 2.35, 0]))
        target = retina.cells[7]
        self.at("removes the working copy")
        self.play(target.bar.animate.set_fill(RED, 1), run_time=0.65)
        self.at("Only that cell's descendants expand")
        cluster = VGroup(*[retinal_cell([x, y, 0], True, True, r=0.34)
                           for x, y in [(-1.35, -0.45), (-0.75, -0.55), (-1.15, -1.05), (-0.55, -1.08)]])
        self.play(*[TransformFromCopy(target, c) for c in cluster], run_time=1.1)
        self.at("Without an inherited first hit")
        panels = TwoPanel("inherited first hit", "two somatic hits", colors=(GOLD, CLAY),
                          top=3.0, bottom=-2.55, size=30)
        left, right = route_panel_cells(True), route_panel_cells(False)
        panels.put(left, "left"), panels.put(right, "right")
        bob(left, amp=0.045, speed=1.05, seed=2)
        bob(right, amp=0.045, speed=1.15, seed=4)
        old_labels = VGroup(*[m for m in self.mobjects if isinstance(m, Text)])
        self.play(FadeOut(VGroup(retina, cluster, old_labels)), run_time=0.3)
        self.play(FadeIn(panels), FadeIn(left), FadeIn(right), run_time=0.7)
        self.at("both hits must arise")
        self.play(Indicate(right[3], color=CLAY, scale_factor=1.08), run_time=0.8)
        self.at("dominant in a family")
        fam = boxed_label("family: risk looks dominant", GOLD, 26).move_to([-3.2, -3.3, 0])
        self.play(FadeIn(fam), run_time=0.55)
        self.at("recessive within a cell")
        cellrule = boxed_label("cell: two losses", RED, 27).move_to([3.25, -2.95, 0])
        self.play(FadeIn(cellrule), run_time=0.55)
        self.finish()


class S09Rule(SpokenScene):
    def construct(self):
        tree = selection_tree(passenger=True).shift(RIGHT * 1.0)
        bob(tree.root, amp=0.13, speed=1.35)
        pulse(tree.links1, base=5, amp=2.5, speed=1.45)
        pulse(tree.links2, base=6, amp=3, speed=1.3)
        accelerator = boxed_label("accelerator ON", BLUE, 29).move_to([-4.7, 2.35, 0])
        brake = boxed_label("brake lost", RED, 29).move_to([-4.7, -2.35, 0])
        bob(accelerator, amp=0.12, speed=1.35, seed=1)
        bob(brake, amp=0.12, speed=1.45, seed=4)
        a1 = Arrow(accelerator.get_right() + RIGHT * 0.24, tree.root.get_left() + UP * 0.12, buff=0.1,
                   color=BLUE, stroke_width=6, tip_length=0.25)
        a2 = Arrow(brake.get_right() + RIGHT * 0.24, tree.root.get_left() + DOWN * 0.12, buff=0.1,
                   color=RED, stroke_width=6, tip_length=0.25)
        self.play(FadeIn(accelerator), FadeIn(brake), run_time=0.6)
        self.at("altered DNA passes")
        self.play(GrowArrow(a1), GrowArrow(a2), FadeIn(tree.root), run_time=0.8)
        self.at("most relevant changes arise somatically")
        self.play(Indicate(tree.root, color=CLAY, scale_factor=1.06), run_time=0.7)
        self.at("accelerator or remove a brake")
        self.play(Indicate(VGroup(accelerator, brake), color=GOLD, scale_factor=1.03), run_time=0.8)
        self.at("Cell lineages expand")
        self.play(Create(tree.links1), FadeIn(tree.level1), run_time=0.8)
        self.at("improved growth or survival")
        self.play(Create(tree.links2), FadeIn(tree.clay), FadeIn(tree.pale), run_time=1.15)
        advantage = boxed_label("growth or survival advantage", CLAY, 30).move_to([0.1, -3.35, 0])
        self.play(FadeOut(accelerator), FadeOut(brake), FadeOut(a1), FadeOut(a2),
                  FadeIn(advantage), run_time=0.7)
        self.at("driver or passenger")
        passenger = Dot(tree.level1[0].get_center() + RIGHT * 0.15, radius=0.075, color=TEXT)
        self.play(FadeIn(passenger), run_time=0.45)
        self.at("spreads with it")
        pd = VGroup(*[Dot(c.get_center() + RIGHT * 0.14, radius=0.06, color=TEXT) for c in tree.clay])
        self.play(*[TransformFromCopy(passenger, q) for q in pd],
                  Indicate(tree.clay, color=CLAY, scale_factor=1.03), run_time=1.1)
        for i, c in enumerate(tree.clay):
            bob(c, amp=0.1, speed=1.2 + i * 0.1, seed=i)
        self.finish()


class S10End(EndCard):
    LINE = "Cell lineages expand when their DNA changes improve growth or survival."
