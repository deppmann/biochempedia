"""Fate, Not Speed — cell-state-and-disease explainer.

COLOR MAP
  BLUE    normal basal progenitors / normal top-down lining
  GREEN   differentiating cells moving toward shedding
  YELLOW  (GOLD in the brief) Notch1-mutant cells and their descendants
  GREY    basement membrane, panels, neutral structure
  TEXT    questions and conclusions

All cell pictures are deliberately schematic; no molecular structures are drawn.
"""
from bp_style import *


GOLDEN = YELLOW
LESSON_NAME = "Cell State and Disease"
BASE_Y = -2.65
XS = np.linspace(-5.75, 2.35, 12)


def cell(color=BLUE, r=0.31, fill=0.58):
    return Circle(radius=r, stroke_color=color, stroke_width=2.4,
                  fill_color=color, fill_opacity=fill)


def clock_face(center, color=TEXT, r=0.14, speed=0.65):
    face = Circle(radius=r, color=color, stroke_width=1.5).move_to(center)
    hand = Line(center, center + UP * r * 0.75, color=color, stroke_width=1.8)
    # Use the live face centre so a zoomed or shifted clock cannot shed its hand.
    hand.add_updater(lambda m, dt: m.rotate(-speed * dt, about_point=face.get_center()))
    return VGroup(face, hand)


def top_sheet(gold_indices=(), label="human donors", clocks=False):
    """Large, frame-filling top view with a gentle per-cell shimmer."""
    cells = VGroup()
    positions = []
    cols, rows = 17, 10
    dx, dy = 0.72, 0.57
    for row in range(rows):
        for col in range(cols):
            x = -5.75 + col * dx + (row % 2) * dx / 2
            y = -2.72 + row * dy
            p = np.array([x, y, 0.0])
            positions.append(p)
            i = row * cols + col
            color = GOLDEN if i in gold_indices else BLUE
            h = RegularPolygon(6, radius=0.36, color=color, stroke_width=1.5,
                               fill_color=color, fill_opacity=0.34)
            h.move_to(p)
            cells.add(h)
    # Shimmer without changing identity colour.
    phase = [0.0]
    def shimmer(group, dt):
        phase[0] += dt
        group.set_stroke(opacity=0.70 + 0.18 * np.sin(phase[0] * 1.4))
    cells.add_updater(shimmer)
    lab = T(label, 30).move_to([-5.9, 3.25, 0], aligned_edge=LEFT)
    note = T("schematic", 28, TEXT).move_to([5.05, -3.45, 0])
    g = VGroup(cells, lab, note)
    g.cells, g.positions, g.label, g.note = cells, positions, lab, note
    if clocks:
        cks = VGroup(*[clock_face(positions[i], TEXT, 0.105, 0.5) for i in [39, 67, 101, 132]])
        g.add(cks)
        g.clocks = cks
    return g


def patch_indices():
    """Irregular connected patches in the 17 by 10 top sheet."""
    patches = [
        [19, 20, 35, 36, 37, 52, 53, 54, 69, 70, 71, 87],
        [76, 77, 78, 92, 93, 94, 95, 109, 110, 111, 126],
        [132, 133, 148, 149, 150, 165, 166],
        [8, 9, 25, 26, 27],
    ]
    return patches


def side_world(gold=(), clocks=True, label=True):
    """The film's stable side-view world; positions are reused scene to scene."""
    floor = Line([-6.1, BASE_Y - 0.37, 0], [2.8, BASE_Y - 0.37, 0],
                 color=GREY, stroke_width=3)
    basal = VGroup()
    clock_group = VGroup()
    for i, x in enumerate(XS):
        color = GOLDEN if i in gold else BLUE
        c = cell(color).move_to([x, BASE_Y, 0])
        basal.add(c)
        if clocks:
            clock_group.add(clock_face(c.get_center(), TEXT, 0.13, 0.62 + (i % 3) * 0.025))
    upper = VGroup()
    for layer in range(1, 6):
        y = BASE_Y + layer * 0.88
        for i, x in enumerate(XS):
            w = 0.56 + layer * 0.085
            h = 0.52 - layer * 0.055
            marked = i in gold
            e = Ellipse(width=w, height=h,
                        stroke_color=GOLDEN if marked else GREEN,
                        stroke_width=2 if marked else 1.6,
                        fill_color=GREEN, fill_opacity=0.31)
            e.move_to([x + (layer % 2) * 0.10, y, 0])
            upper.add(e)
    # Slow escalator drift and shimmer, enough to keep long explanatory holds alive.
    phase = [0.0]
    def breathe(group, dt):
        phase[0] += dt
        group.set_fill(opacity=0.28 + 0.07 * (1 + np.sin(phase[0] * 1.1)) / 2)
        group.shift(UP * 0.006 * dt)
    upper.add_updater(breathe)
    world = VGroup(floor, upper, basal, clock_group)
    world.floor, world.upper, world.basal, world.clocks = floor, upper, basal, clock_group
    if label:
        lab = T("mouse oesophagus", 28).move_to([-5.9, 3.25, 0], aligned_edge=LEFT)
        world.add(lab)
        world.label = lab
    return world


def panel_frame():
    return RoundedRectangle(width=3.2, height=5.9, corner_radius=0.18,
                            color=GREY, stroke_width=1.8).move_to([4.65, 0, 0])


def outcome_tile(kind, color=BLUE, scale=1.0):
    box = RoundedRectangle(width=2.55, height=1.45, corner_radius=0.16,
                           color=color, stroke_width=2, fill_color=color, fill_opacity=0.06)
    parent = cell(color, 0.16).move_to(box.get_left() + RIGHT * 0.42 + UP * 0.16)
    arrow = Arrow(parent.get_right() + RIGHT * 0.05, parent.get_right() + RIGHT * 0.55,
                  buff=0, color=GREY, stroke_width=2, max_tip_length_to_length_ratio=0.3)
    kids = VGroup()
    cols = [color, color] if kind == "PP" else ([color, GREEN] if kind == "PD" else [GREEN, GREEN])
    for j, col in enumerate(cols):
        kid = cell(col, 0.15).move_to(box.get_center() + [0.28 + j * 0.38, 0.06 if col == color else 0.38, 0])
        kids.add(kid)
    lab = T(kind, 36, color).move_to(box.get_bottom() + UP * 0.28)
    return VGroup(box, parent, arrow, kids, lab).scale(scale)


def question_card():
    q = T("Hold steady,\ndie out,\nor spread?", 28, line_spacing=0.9)
    box = RoundedRectangle(width=3.05, height=2.2, corner_radius=0.18,
                           color=TEXT, fill_color=TEXT, fill_opacity=0.04)
    return VGroup(box, q.move_to(box)).move_to([4.65, 0.35, 0])


class S00Hook(SpokenScene):
    def construct(self):
        sheet = top_sheet()
        self.play(FadeIn(sheet), run_time=0.8)
        self.at("much of the healthy")
        patches = patch_indices()
        for patch in patches:
            self.play(*[sheet.cells[i].animate.set_stroke(GOLDEN).set_fill(GOLDEN, 0.50)
                        for i in patch[:max(2, len(patch)//2)]], run_time=0.55)
        self.at("mutation in one cancer")
        self.play(*[sheet.cells[i].animate.set_stroke(GOLDEN).set_fill(GOLDEN, 0.50)
                    for patch in patches for i in patch], run_time=0.9)
        clone_lab = T("NOTCH1-mutant: est. 12–80%", 28, GOLDEN).move_to([3.2, 3.40, 0])
        source = T("Martincorena et al., 2018", 22, TEXT).next_to(clone_lab, DOWN, buff=0.08)
        self.play(FadeIn(clone_lab), FadeIn(source), run_time=0.45)
        self.at("How does one mutant")
        question = T("How does one family fill it?", 38).move_to([0, 3.18, 0])
        self.play(FadeOut(sheet.label), FadeOut(clone_lab), FadeOut(source),
                  FadeIn(question, shift=DOWN * 0.1), run_time=0.55)
        self.finish()


class S01Title(TitleCard):
    LESSON = LESSON_NAME
    TITLE = "Fate, Not Speed"

    def construct(self):
        gold = [i for p in patch_indices() for i in p]
        sheet = top_sheet(gold, label="")
        sheet.remove(sheet.label, sheet.note)
        sheet.set_opacity(0.34)
        title = T(self.TITLE, 58, font=TITLE_FONT)
        lesson = T(self.LESSON.upper(), 24, TEAL)
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4)
        card = VGroup(lesson, title, rule).arrange(DOWN, buff=0.32)
        self.add(sheet)
        self.play(FadeIn(card, shift=UP * 0.12), run_time=0.55)
        self.finish()


class S02World(SpokenScene):
    def construct(self):
        sheet = top_sheet(label="human donors")
        self.add(sheet)
        self.at("Experiments in mouse")
        world = side_world()
        self.play(FadeOut(sheet), FadeIn(world, shift=UP * 0.12), run_time=1.0)
        self.at("Here is the lining")
        self.play(Indicate(VGroup(world.basal, world.upper), color=TEXT), run_time=0.7)
        self.at("Only the bottom row")
        self.play(Indicate(world.basal, color=BLUE, scale_factor=1.07), run_time=0.75)
        self.at("That row is the basal")
        basal_lab = T("basal layer", 30, BLUE).move_to([-4.9, -3.42, 0])
        self.play(FadeIn(basal_lab, shift=RIGHT * 0.15), run_time=0.45)
        self.at("dividing cells are")
        i = 6
        two = VGroup(cell(BLUE, 0.25), cell(BLUE, 0.25)).arrange(RIGHT, buff=0.10).move_to(world.basal[i])
        self.play(ReplacementTransform(world.basal[i], two), run_time=0.55)
        prog = T("progenitor", 28, BLUE).move_to([4.65, 1.6, 0])
        pointer = Arrow(prog.get_left(), two.get_top(), buff=0.15, color=BLUE, stroke_width=2.5)
        self.play(FadeIn(prog), GrowArrow(pointer), run_time=0.35)
        self.finish()


class S03Conveyor(SpokenScene):
    def construct(self):
        world = side_world()
        self.add(world)
        i = 6
        self.at("Each daughter")
        daughters = VGroup(cell(BLUE, 0.25), cell(BLUE, 0.25)).arrange(RIGHT, buff=0.08).move_to(world.basal[i])
        self.play(ReplacementTransform(world.basal[i], daughters), run_time=0.65)
        self.at("or leaves it")
        leaving = daughters[1]
        self.play(leaving.animate.set_color(GREEN).set_fill(GREEN, 0.55).shift(UP * 0.8), run_time=0.65)
        diff_lab = T("differentiating", 28, GREEN).move_to([4.65, 1.8, 0])
        self.play(FadeIn(diff_lab), run_time=0.25)
        self.at("Cells that leave")
        self.play(leaving.animate.shift(UP * 1.45).stretch(1.35, 0), diff_lab.animate.shift(DOWN * 0.55), run_time=1.0)
        self.at("ride upward")
        self.play(leaving.animate.shift(UP * 1.6).stretch(1.25, 0).stretch(0.72, 1),
                  FadeOut(diff_lab), run_time=1.0)
        self.at("shed from the top")
        self.play(leaving.animate.shift(UP * 1.2), FadeOut(leaving), run_time=0.8)
        self.at("cell number steady")
        frame = panel_frame()
        made_lab, shed_lab = T("made", 28, BLUE), T("shed", 28, GREEN)
        made_num, shed_num = M("0", 38, BLUE), M("0", 38, GREEN)
        counters = VGroup(VGroup(made_lab, made_num).arrange(DOWN, buff=0.2),
                          VGroup(shed_lab, shed_num).arrange(DOWN, buff=0.2)).arrange(RIGHT, buff=0.55).move_to(frame)
        self.play(Create(frame), FadeIn(counters), run_time=0.5)
        self.at("makes as many")
        for n in [1, 2, 3]:
            self.play(Transform(made_num, M(str(n), 38, BLUE).move_to(made_num)),
                      Transform(shed_num, M(str(n), 38, GREEN).move_to(shed_num)), run_time=0.35)
        self.finish()


class S04Outcomes(SpokenScene):
    def construct(self):
        world = side_world()
        frame = panel_frame()
        self.add(world, frame)
        self.at("Watch one progenitor")
        self.play(Indicate(world.basal[5], color=BLUE), run_time=0.7)
        title = T("division outcomes", 28).move_to([4.65, 3.15, 0])
        self.at("three possible outcomes")
        self.play(FadeIn(title), run_time=0.4)
        tiles = [outcome_tile(k).move_to([4.65, y, 0]) for k, y in zip(["PP", "PD", "DD"], [1.75, 0.15, -1.45])]
        self.at("Both daughters stay")
        self.play(FadeIn(tiles[0], shift=RIGHT * 0.2), run_time=0.65)
        self.at("One stays and one leaves")
        self.play(FadeIn(tiles[1], shift=RIGHT * 0.2), run_time=0.65)
        self.at("Or both leave")
        self.play(FadeIn(tiles[2], shift=RIGHT * 0.2), run_time=0.65)
        self.finish()


class S05Balance(SpokenScene):
    def construct(self):
        world = side_world()
        frame = panel_frame()
        tiles = [outcome_tile(k, scale=0.82).move_to([4.65, y, 0]) for k, y in zip(["PP", "PD", "DD"], [2.3, 0.9, -0.5])]
        self.add(world, frame, *tiles)
        self.at("outcomes are balanced")
        balance = Line([3.55, -1.45, 0], [5.75, -1.45, 0], color=TEXT, stroke_width=3)
        self.play(Create(balance), Indicate(VGroup(tiles[0], tiles[2]), color=TEXT), run_time=0.8)
        self.at("PP comes up")
        self.play(tiles[0].animate.set_fill(GOLDEN, 0.15), tiles[2].animate.set_fill(GOLDEN, 0.15), run_time=0.55)
        tally_title = T("progenitors left", 28).move_to([4.65, -1.8, 0])
        dots = VGroup(*[cell(BLUE, 0.12) for _ in range(3)]).arrange(RIGHT, buff=0.16).move_to([4.65, -2.3, 0])
        self.at("each division leaves")
        self.play(FadeIn(tally_title), FadeIn(dots[0]), run_time=0.4)
        self.play(FadeIn(dots[1:]), FadeOut(dots[1:]), run_time=0.55)
        one = M("average: 1", 28, BLUE).move_to([4.65, -2.8, 0])
        self.play(FadeIn(one), run_time=0.35)
        self.at("One in one out")
        line = T("one in, one out", 30).move_to([0, 3.25, 0])
        self.play(FadeIn(line), Indicate(world.basal, color=BLUE), run_time=0.7)
        self.finish()


class S06Gold(SpokenScene):
    def construct(self):
        world = side_world()
        self.add(world)
        i = 6
        self.at("loses notch one")
        self.play(world.basal[i].animate.set_color(GOLDEN).set_fill(GOLDEN, 0.62), Flash(world.basal[i], color=GOLDEN), run_time=0.7)
        lost = T("Notch1 lost", 30, GOLDEN).move_to([XS[i] + 0.7, -3.42, 0])
        arrow = Arrow(lost.get_top(), world.basal[i].get_bottom(), buff=0.10, color=GOLDEN)
        self.at("mark it gold")
        self.play(FadeIn(lost), GrowArrow(arrow), run_time=0.45)
        self.at("Every cell descended")
        stay = cell(GOLDEN, 0.27).move_to(world.basal[i].get_center() + LEFT * 0.18)
        rise = cell(GREEN, 0.27).set_stroke(GOLDEN, 3).move_to(world.basal[i].get_center() + RIGHT * 0.18)
        self.play(ReplacementTransform(world.basal[i], VGroup(stay, rise)), run_time=0.55)
        self.play(rise.animate.shift(UP * 1.45).stretch(1.2, 0), run_time=0.8)
        self.at("family of cells")
        outline = DashedVMobject(SurroundingRectangle(VGroup(stay, rise), buff=0.22, color=GOLDEN), num_dashes=18)
        clone = T("clone", 34, GOLDEN).move_to([4.65, 0.25, 0])
        self.play(Create(outline), FadeIn(clone), run_time=0.55)
        self.finish()


class S07Clock(SpokenScene):
    def construct(self):
        # Close-up retains the same left-to-right order and equal clock scale.
        centers = [[-3.2, 0, 0], [0, 0, 0], [3.2, 0, 0]]
        bodies = VGroup(cell(BLUE, 1.15), cell(GOLDEN, 1.15), cell(BLUE, 1.15))
        for b, p in zip(bodies, centers): b.move_to(p)
        clocks = VGroup(*[clock_face(np.array(p), TEXT, 0.62, s) for p, s in zip(centers, [0.64, 0.62, 0.66])])
        self.add(bodies, clocks)
        self.at("runs no faster")
        # This group later scales to 62%; start large so the carried label
        # remains comfortably above the 28 pt reading minimum.
        label = T("no faster", 48, GOLDEN).move_to([0, -1.75, 0])
        self.play(FadeIn(label), Indicate(bodies[1], color=GOLDEN), run_time=0.6)
        self.at("one difference")
        self.play(VGroup(bodies, clocks, label).animate.scale(0.62).shift(LEFT * 2.7), run_time=0.75)
        frame = panel_frame()
        pp = outcome_tile("PP", GOLDEN, 1.04).move_to([4.65, 1.25, 0])
        dd = outcome_tile("DD", GOLDEN, 0.82).move_to([4.65, -1.0, 0])
        self.play(Create(frame), FadeIn(pp), FadeIn(dd), run_time=0.65)
        self.at("PP a little more")
        schematic = T("schematic", 28, TEXT).move_to([4.65, -3.25, 0])
        self.play(pp.animate.scale(1.08), dd.animate.scale(0.92), FadeIn(schematic), run_time=0.55)
        self.finish()


class S08Question(SpokenScene):
    def construct(self):
        world = side_world(gold=[6])
        self.add(world)
        self.at("a question")
        card = question_card()
        self.play(FadeIn(card, shift=LEFT * 0.2), run_time=0.6)
        self.at("will the gold clone")
        self.play(Indicate(world.basal[6], color=GOLDEN), run_time=0.55)
        self.at("hold steady")
        self.play(card.animate.set_stroke(GOLDEN), run_time=0.45)
        self.finish()


class S09Pause(Scene):
    def construct(self):
        world = side_world(gold=[6])
        card = question_card()
        self.add(world, card)
        self.wait(4.5)


class S10Reveal(SpokenScene):
    def construct(self):
        world = side_world(gold=[6])
        card = question_card()
        self.add(world, card)
        self.at("it spreads")
        answer = T("It spreads", 38, GOLDEN).move_to(card)
        self.play(Transform(card, VGroup(SurroundingRectangle(answer, buff=0.3, color=GOLDEN), answer)), run_time=0.65)
        self.at("simplest picture")
        tag = T("simplest picture • schematic", 28, TEXT).move_to([3.80, -3.45, 0])
        time = VGroup(T("time", 28), Arrow(LEFT * 0.7, RIGHT * 0.7, color=TEXT, buff=0)).arrange(RIGHT, buff=0.18).move_to([4.65, 2.9, 0])
        self.play(FadeOut(card), FadeIn(tag), FadeIn(time), run_time=0.55)
        self.at("each division leaves")
        # Replace the same row positions, never drifting the world.
        for inds in [[5, 6], [4, 5, 6, 7], [3, 4, 5, 6, 7, 8, 9]]:
            self.play(*[world.basal[i].animate.set_color(GOLDEN).set_fill(GOLDEN, 0.62) for i in inds], run_time=0.62)
        self.at("Round after round")
        marked = VGroup(*[Ellipse(width=0.75, height=0.38, color=GOLDEN, stroke_width=2,
                                  fill_color=GREEN, fill_opacity=0.3).move_to([XS[i], -0.9 + (i % 3) * 0.75, 0])
                          for i in range(3, 10)])
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.5) for m in marked], lag_ratio=0.08), run_time=1.1)
        self.at("watch the edges")
        left_i, right_i = 2, 10
        self.play(Indicate(VGroup(world.basal[left_i], world.basal[right_i]), color=TEXT), run_time=0.6)
        self.at("Blue neighbors")
        self.play(world.basal[left_i].animate.set_color(GREEN).shift(UP * 0.85),
                  world.basal[right_i].animate.set_color(GREEN).shift(UP * 0.85), run_time=0.8)
        gold_l = cell(GOLDEN).move_to([XS[left_i], BASE_Y, 0])
        gold_r = cell(GOLDEN).move_to([XS[right_i], BASE_Y, 0])
        self.play(FadeIn(gold_l, shift=RIGHT * 0.25), FadeIn(gold_r, shift=LEFT * 0.25), run_time=0.55)
        self.finish()


class S11Room(SpokenScene):
    def construct(self):
        world = side_world(gold=range(2, 11))
        self.add(world)
        edge = world.basal[1]
        gap = DashedVMobject(Circle(radius=0.35, color=TEXT).move_to(edge), num_dashes=12)
        self.at("takes room")
        self.play(edge.animate.set_color(GREEN).shift(UP * 0.9), FadeIn(gap), run_time=0.75)
        room = T("room given up", 28).move_to([-4.75, -3.42, 0])
        arr = Arrow(room.get_top(), gap.get_bottom(), buff=0.10, color=TEXT)
        self.at("neighbor gives up")
        self.play(FadeIn(room), GrowArrow(arr), run_time=0.4)
        replacement = cell(GOLDEN).move_to([XS[1], BASE_Y, 0])
        self.play(FadeIn(replacement, shift=RIGHT * 0.35), FadeOut(gap), run_time=0.65)
        self.at("keeping more of its daughters")
        pp = outcome_tile("PP", GOLDEN, 1.05).move_to([4.65, -0.1, 0])
        self.play(FadeIn(pp), Indicate(pp, color=GOLDEN), run_time=0.65)
        nofast = T("clocks: no faster", 28, BLUE).move_to([4.65, -1.65, 0])
        self.play(FadeIn(nofast), run_time=0.35)
        self.at("Fate not speed")
        idea = T("Fate, not speed", 40, GOLDEN).move_to([4.65, -2.65, 0])
        self.play(FadeIn(idea, shift=UP * 0.12), run_time=0.55)
        self.finish()


class S12Pullback(SpokenScene):
    def construct(self):
        world = side_world(gold=range(2, 11))
        self.add(world)
        self.at("look down on the lining")
        sheet = top_sheet(label="mouse oesophagus", clocks=True)
        self.play(FadeOut(world), FadeIn(sheet), run_time=0.9)
        patches = patch_indices()
        self.at("With time")
        # One seed disappears; the other three expand in visibly separate rounds.
        seeds = [p[0] for p in patches]
        self.play(*[sheet.cells[i].animate.set_color(GOLDEN).set_fill(GOLDEN, 0.52) for i in seeds], run_time=0.45)
        self.play(sheet.cells[seeds[-1]].animate.set_color(BLUE).set_fill(BLUE, 0.34),
                  *[sheet.cells[i].animate.set_color(GOLDEN).set_fill(GOLDEN, 0.52)
                    for p in patches[:3] for i in p[:len(p)//2]], run_time=0.8)
        self.at("patches spread")
        self.play(*[sheet.cells[i].animate.set_color(GOLDEN).set_fill(GOLDEN, 0.52)
                    for p in patches[:3] for i in p], run_time=0.9)
        self.at("which cells are there")
        gold_cells = VGroup(*[sheet.cells[i] for p in patches[:3] for i in p])
        self.play(Indicate(gold_cells, color=GOLDEN, scale_factor=1.025), run_time=0.65)
        self.at("divided no faster")
        nofast = T("same clock rate", 32).move_to([4.55, 3.15, 0])
        self.play(FadeIn(nofast), Indicate(sheet.clocks, color=TEXT), run_time=0.55)
        self.finish()


class S13Handoff(SpokenScene):
    def construct(self):
        gold = [i for p in patch_indices()[:3] for i in p]
        sheet = top_sheet(gold, label="mouse oesophagus")
        sheet.remove(sheet.label, sheet.note)
        sheet.scale(0.62).move_to([-3.15, -0.15, 0])
        context = T("mouse oesophagus • schematic", 28).move_to([-3.15, 2.25, 0])
        self.add(sheet, context)
        self.at("clones dangerous")
        q1 = T("Dangerous?", 38).move_to([3.65, 1.5, 0])
        self.play(FadeIn(q1, shift=LEFT * 0.15), run_time=0.5)
        self.at("tell fate from speed")
        q2 = T("Fate or speed:\nhow to tell?", 34, line_spacing=1.0).move_to([3.65, 0, 0])
        self.play(FadeIn(q2, shift=LEFT * 0.15), run_time=0.55)
        self.at("text below")
        down = Arrow([3.65, -1.0, 0], [3.65, -2.25, 0], color=GOLDEN, stroke_width=5)
        lab = T("in the text", 30, GOLDEN).next_to(down, DOWN, buff=0.15)
        self.play(GrowArrow(down), FadeIn(lab), run_time=0.6)
        self.finish()


class S14End(EndCard):
    LINE = "In this lining, a clone spreads by fate, not by speed."

    def construct(self):
        line = T(self.LINE, 40, font=TITLE_FONT).move_to([0.9, 0, 0])
        fit(line, max_w=9.8)
        patch = VGroup(*[
            RegularPolygon(6, radius=0.30, color=GOLDEN, stroke_width=2,
                           fill_color=GOLDEN, fill_opacity=0.42)
            for _ in range(7)
        ])
        for h, p in zip(patch, [(-0.36, 0, 0), (0.36, 0, 0), (0, 0.53, 0),
                                (0, -0.53, 0), (-0.72, 0.53, 0), (-0.72, -0.53, 0),
                                (0.72, 0.53, 0)]):
            h.move_to(p)
        patch.move_to([-5.55, 0, 0])
        phase = [0.0]

        def shimmer(group, dt):
            phase[0] += dt
            group.set_stroke(opacity=0.72 + 0.20 * np.sin(phase[0] * 1.5))

        patch.add_updater(shimmer)
        self.play(FadeIn(patch, shift=RIGHT * 0.15), FadeIn(line, shift=UP * 0.1),
                  run_time=self.beat(0.35))
        self.finish()
