"""The First Split — domains and kingdoms.

COLOR MAP
  GOLD  = Eukarya
  BLUE  = Bacteria
  TEAL  = Archaea
  TEXT  = trait evidence
  RED   = limits and stop signs
"""
from bp_parts import *


CELL_R = 1.18


def mystery_cell(color=TEAL, center=ORIGIN, radius=CELL_R, dna=True, nucleus=False):
    """The carried mystery-cell picture, rebuilt at one scale and position."""
    c = np.array(center, dtype=float)
    membrane = Circle(radius=radius, color=color, stroke_width=7,
                      fill_color=color, fill_opacity=0.24).move_to(c)
    cytoplasm = VGroup(*[
        Dot(c + radius * np.array([-.42, .36, 0]), radius=.07, color=TEXT),
        Dot(c + radius * np.array([.42, .25, 0]), radius=.06, color=TEXT),
        Dot(c + radius * np.array([-.25, -.45, 0]), radius=.055, color=TEXT),
    ]).set_opacity(.65)
    parts = VGroup(membrane, cytoplasm)
    if dna:
        bar = RoundedRectangle(corner_radius=.08, width=1.15 * radius, height=.18,
                               stroke_width=0, fill_color=TEXT, fill_opacity=.95).move_to(c + DOWN * .08)
        dna_label = T("DNA", 28, TEXT, weight=BOLD).next_to(bar, DOWN, buff=.13)
        parts.add(bar, dna_label)
    if nucleus:
        nuc = Circle(radius=.61 * radius, color=GOLD, stroke_width=6,
                     fill_color=GOLD, fill_opacity=.17).move_to(c)
        parts.add(nuc)
    parts.membrane = membrane
    return parts


def drifting(mob, amp=.14, speed=.65, phase=0.0):
    """Slow two-axis drift around the object's built position."""
    base = mob.get_center().copy()
    mob._drift_t = phase
    def update(m, dt):
        m._drift_t += dt
        m.move_to(base + RIGHT * amp * np.sin(speed * m._drift_t)
                  + UP * amp * .55 * np.sin(speed * .73 * m._drift_t + phase))
    mob.add_updater(update)
    return mob


def travel_dot(path, color, speed=.08, phase=0.0):
    """A small evidence marker continuously travelling along a branch."""
    dot = Dot(path.point_from_proportion(phase), radius=.18, color=color)
    dot._travel_t = phase
    def update(m, dt):
        m._travel_t = (m._travel_t + speed * dt) % 1.0
        m.move_to(path.point_from_proportion(m._travel_t))
    dot.add_updater(update)
    return dot


def pond_world(with_path=True):
    """Large pond drop used by the hook and title at identical coordinates."""
    drop = Circle(radius=3.0, color=TEXT, stroke_width=6,
                  fill_color=BLUE, fill_opacity=.18).move_to([-1.3, -.25, 0])
    cells = VGroup(
        mystery_cell(GOLD, [-2.55, .65, 0], .55, dna=False),
        mystery_cell(BLUE, [-.35, .65, 0], .48, dna=False),
        mystery_cell(TEAL, [-1.55, -1.45, 0], .58, dna=False),
        mystery_cell(BLUE, [-3.05, -1.35, 0], .34, dna=False),
        mystery_cell(TEAL, [.05, -1.35, 0], .31, dna=False),
    )
    for i, cell in enumerate(cells):
        drifting(cell, amp=.12 + .015 * i, speed=.55 + .06 * i, phase=i)
    world = VGroup(drop, cells)
    world.drop, world.cells = drop, cells
    if with_path:
        path = VMobject(color=TEXT, stroke_width=7).set_points_smoothly([
            drop.get_right() + LEFT * .15,
            [2.25, .25, 0], [3.15, 1.25, 0], [4.2, .45, 0], [5.15, 1.5, 0]
        ])
        q = T("?", 70, GOLD, weight=BOLD).move_to([5.45, 1.75, 0])
        world.add(path, q)
        world.path, world.question = path, q
    return world


def microscope_pair():
    """Blue and teal look-alike cells in the shared microscope field."""
    field = Circle(radius=2.85, color=TEXT, stroke_width=6,
                   fill_color=TEXT, fill_opacity=.09).move_to([0, .25, 0])
    blue = mystery_cell(BLUE, [-1.55, .25, 0], 1.05, dna=True)
    teal = mystery_cell(TEAL, [1.55, .25, 0], 1.05, dna=True)
    pair = VGroup(field, blue, teal)
    pair.field, pair.blue, pair.teal = field, blue, teal
    return pair


SEQ = list("ACGUACGA")
DIFFS = {2, 6}


def sequence_strips():
    """Aligned schematic rRNA strips, with every position computed from SEQ."""
    def row(y, color, archaea=False):
        blocks = VGroup()
        for i, base in enumerate(SEQ):
            letter = ("U" if i == 2 else "C" if i == 6 else base) if archaea else base
            box = RoundedRectangle(corner_radius=.08, width=.86, height=.8,
                                   color=color if i in DIFFS else TEXT, stroke_width=4,
                                   fill_color=color if i in DIFFS else TEXT, fill_opacity=.20)
            lab = M(letter, 32, color if i in DIFFS else TEXT).move_to(box)
            lab.layout_ok = True
            blocks.add(VGroup(box, lab))
        blocks.arrange(RIGHT, buff=.12).move_to([.45, y, 0])
        return blocks
    b, a = row(.85, BLUE), row(-.65, TEAL, True)
    labels = VGroup(T("Bacteria", 30, BLUE, weight=BOLD).move_to([-5.1, .85, 0]),
                    T("Archaea", 30, TEAL, weight=BOLD).move_to([-5.1, -.65, 0]))
    tag = scope_tag("schematic")
    g = VGroup(b, a, labels, tag)
    g.blue, g.teal, g.labels, g.tag = b, a, labels, tag
    return g


def evidence_block(text, color=TEXT, width=3.7):
    label = fit_text(text, max_w=width - .4, size=28, min_size=24, color=color, max_lines=2)
    box = RoundedRectangle(corner_radius=.16, width=width,
                           height=max(.72, label.height + .34), color=color, stroke_width=4,
                           fill_color=color, fill_opacity=.20)
    label.move_to(box)
    label.layout_ok = True
    return VGroup(box, label)


def chemistry_panels():
    panels = TwoPanel("Bacteria", "Archaea", colors=(BLUE, TEAL), top=3.15, bottom=-2.45)
    blue = mystery_cell(BLUE, [-3.3, 1.05, 0], .75, dna=False)
    teal = mystery_cell(TEAL, [3.3, 1.05, 0], .75, dna=False)
    b1 = evidence_block("peptidoglycan", BLUE, 4.5).move_to([-3.3, -.25, 0])
    a1 = evidence_block("no peptidoglycan", TEAL, 4.5).move_to([3.3, -.25, 0])
    b2 = evidence_block("typical ester link", BLUE, 4.5).move_to([-3.3, -1.45, 0])
    a2 = evidence_block("typical ether link", TEAL, 4.5).move_to([3.3, -1.45, 0])
    g = VGroup(panels, blue, teal, b1, a1, b2, a2)
    g.panels, g.cells = panels, VGroup(blue, teal)
    g.wall_blocks, g.link_blocks = VGroup(b1, a1), VGroup(b2, a2)
    return g


def domain_tree():
    """Equal-height schematic domain tree with the Archaea/Eukarya shared fork."""
    root = np.array([0, -2.45, 0])
    j1, j2 = np.array([0, -1.25, 0]), np.array([1.65, .05, 0])
    tips = [np.array([-4.1, 2.35, 0]), np.array([1.25, 2.35, 0]), np.array([4.35, 2.35, 0])]
    branches = VGroup(
        Line(root, j1, color=TEXT, stroke_width=8),
        VMobject(color=BLUE, stroke_width=8).set_points_smoothly([j1, [-2.2, -.5, 0], tips[0]]),
        Line(j1, j2, color=TEXT, stroke_width=8),
        VMobject(color=TEAL, stroke_width=8).set_points_smoothly([j2, [.9, 1.05, 0], tips[1]]),
        VMobject(color=GOLD, stroke_width=8).set_points_smoothly([j2, [3.05, 1.05, 0], tips[2]]),
    )
    labels = VGroup(T("Bacteria", 34, BLUE, weight=BOLD).next_to(tips[0], UP, buff=.18),
                    T("Archaea", 34, TEAL, weight=BOLD).next_to(tips[1], UP, buff=.18),
                    T("Eukarya", 34, GOLD, weight=BOLD).next_to(tips[2], UP, buff=.18))
    root_label = T("shared root", 28, TEXT).next_to(root, DOWN, buff=.22)
    tag = scope_tag("schematic")
    g = VGroup(branches, labels, root_label, tag)
    g.branches, g.labels, g.root_label, g.tag = branches, labels, root_label, tag
    return g


def ordered_path():
    """The film's final decision path, reused unchanged in the final spoken scene."""
    xs = [-5.2, -1.8, 1.8, 5.2]
    ys = [1.55, 1.55, -.05, 1.55]
    labels = ["mystery cell", "nucleus?", "looks reach limit", "molecular evidence"]
    cols = [TEXT, GOLD, RED, TEAL]
    nodes = VGroup(*[evidence_block(s, c, 2.45).move_to([x, y, 0])
                     for x, y, s, c in zip(xs, ys, labels, cols)])
    arrows = VGroup(*[Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), buff=.12,
                            color=TEXT, stroke_width=5, tip_length=.22)
                      for i in range(3)])
    return VGroup(nodes, arrows)


class S00Hook(SpokenScene):
    def construct(self):
        world = pond_world(False)
        self.play(Create(world.drop), run_time=.9)
        self.at("may hold cells")
        self.play(LaggedStart(*[FadeIn(c, scale=.7) for c in world.cells], lag_ratio=.15), run_time=1.4)
        self.at("Which question")
        path_world = pond_world(True)
        self.play(Create(path_world.path), FadeIn(path_world.question), run_time=1.2)
        self.at("cells drift together")
        self.play(Indicate(world.drop, color=TEXT, scale_factor=1.02), run_time=1.0)
        self.at("useful key needs")
        forks = VGroup(*[Dot(path_world.path.point_from_proportion(p), radius=.11, color=TEXT)
                         for p in (.25, .5, .75)])
        self.play(LaggedStart(*[GrowFromCenter(x) for x in forks], lag_ratio=.2), run_time=1.0)
        self.at("one mystery cell")
        self.play(Indicate(world.cells[2], color=TEAL, scale_factor=1.25), run_time=1.0)
        self.at("open the next path")
        self.play(ShowPassingFlash(path_world.path.copy().set_stroke(GOLD, 12), time_width=.5), run_time=1.6)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Domains and Kingdoms"
    TITLE = "The First Split"

    def construct(self):
        world = pond_world(False).set_opacity(.28)
        title = T(self.TITLE, 58, TEXT, font=TITLE_FONT)
        lesson = T(self.LESSON.upper(), 24, GOLD, weight=BOLD).next_to(title, UP, buff=.35)
        title.layout_ok = True
        lesson.layout_ok = True
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=5).next_to(title, DOWN, buff=.35)
        self.add(world)
        self.play(FadeIn(lesson), Write(title), GrowFromCenter(rule), run_time=1.1)
        self.wait(.45)
        self.play(FadeOut(VGroup(lesson, title, rule)), run_time=.35)
        self.finish()


class S02Nucleus(SpokenScene):
    def construct(self):
        cell = mystery_cell(GOLD, [0, .45, 0], 2.35, dna=True, nucleus=False)
        self.play(FadeIn(cell.membrane), FadeIn(cell[1]), run_time=.9)
        self.at("light microscope")
        lens = Circle(radius=2.85, color=TEXT, stroke_width=6).move_to([0, .45, 0])
        self.play(Create(lens), run_time=.8)
        pulse(lens, base=6, amp=1.2, speed=1.3)
        self.at("A nucleus")
        nucleus = Circle(radius=1.35, color=GOLD, stroke_width=8,
                         fill_color=GOLD, fill_opacity=.18).move_to([0, .45, 0])
        self.play(GrowFromCenter(nucleus), run_time=1.0)
        self.at("holding the DNA")
        self.play(FadeIn(cell[2]), FadeIn(cell[3]), run_time=.7)
        self.at("belongs in Eukarya")
        euk = evidence_block("Eukarya", GOLD, 3.0).move_to([4.7, .45, 0])
        arrow = Arrow(lens.get_right(), euk.get_left(), buff=.12, color=GOLD, stroke_width=6)
        self.play(GrowArrow(arrow), FadeIn(euk), run_time=.9)
        self.at("If it does not")
        no_nucleus = mystery_cell(TEAL, [0, .45, 0], 2.35, dna=True, nucleus=False)
        self.play(FadeOut(nucleus), FadeOut(euk), FadeOut(arrow),
                  Transform(cell, no_nucleus), run_time=1.0)
        self.at("organism is a prokaryote")
        pro = evidence_block("prokaryote", TEXT, 3.3).move_to([4.65, .45, 0])
        self.play(FadeIn(pro, shift=LEFT * .2), run_time=.7)
        self.at("sits in the cytoplasm")
        self.play(Indicate(cell[2], color=TEXT, scale_factor=1.18), run_time=1.0)
        self.finish()


class S03Prokaryotes(SpokenScene):
    def construct(self):
        pair = microscope_pair()
        drifting(pair.blue, amp=.055, speed=.68)
        drifting(pair.teal, amp=.055, speed=.74, phase=2)
        self.play(FadeIn(pair.field), FadeIn(pair.teal), run_time=.9)
        self.at("no nucleus")
        no = T("no nucleus", 32, TEXT, weight=BOLD).move_to([0, 3.35, 0])
        self.play(FadeIn(no), run_time=.6)
        self.at("rules out Eukarya")
        gold = T("Eukarya", 32, GOLD).move_to([-4.9, 2.7, 0])
        strike = Line(gold.get_left(), gold.get_right(), color=RED, stroke_width=7)
        strike.layout_ok = True
        self.play(FadeIn(gold), Create(strike), run_time=.8)
        self.at("Bacteria and Archaea remain")
        self.play(FadeIn(pair.blue), FadeOut(VGroup(gold, strike)), run_time=.9)
        self.at("made up of prokaryotes")
        labs = VGroup(T("Bacteria", 28, BLUE, weight=BOLD).next_to(pair.blue, DOWN, buff=.14).shift(RIGHT * .22),
                      T("Archaea", 28, TEAL, weight=BOLD).next_to(pair.teal, DOWN, buff=.14).shift(LEFT * .3))
        self.play(FadeIn(labs), run_time=.7)
        self.at("single cells")
        self.play(Indicate(pair.blue.membrane, color=BLUE), Indicate(pair.teal.membrane, color=TEAL), run_time=.9)
        self.at("chains or filaments")
        ghosts = VGroup(*[mystery_cell(BLUE if i < 3 else TEAL,
                                      [-4.9 + (i % 3) * .65, -2.55, 0], .24, dna=False)
                          for i in range(6)])
        self.play(LaggedStart(*[FadeIn(g) for g in ghosts], lag_ratio=.12), run_time=1.0)
        self.play(FadeOut(ghosts), run_time=.5)
        self.at("can look alike")
        self.play(Indicate(pair.field, color=TEXT, scale_factor=1.01), run_time=1.2)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        pair = microscope_pair()
        drifting(pair.blue, amp=.055, speed=.68)
        drifting(pair.teal, amp=.055, speed=.74, phase=2)
        self.add(pair)
        self.at("shapes and sizes")
        self.play(Rotate(pair.blue, angle=.35), Rotate(pair.teal, angle=-.35), run_time=1.3)
        self.at("Can the microscope alone")
        q = question_card("Can looks decide?", ["YES", "NO"], y=-3.2, size=34,
                          chips_at=[4.75, 0, 0])
        self.play(FadeIn(q.question), run_time=.6)
        self.at("bacteria and the other")
        self.play(FadeIn(q.chips), run_time=.7)
        self.at("Choose yes or no")
        self.play(Indicate(q.chips, color=GOLD, scale_factor=1.05), run_time=1.1)
        self.at("evidence you trust")
        self.play(Rotate(pair.blue, angle=.25), Rotate(pair.teal, angle=-.25), run_time=1.3)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Can looks decide?"
    OPTIONS = ["YES", "NO"]
    CHIPS_AT = [4.75, 0, 0]
    SECONDS = 4.5
    CARD = {"y": -3.2, "size": 34}

    def backdrop(self):
        pair = microscope_pair()
        drifting(pair.blue, amp=.06, speed=.7)
        drifting(pair.teal, amp=.06, speed=.75, phase=2)
        return pair


class S06Sequence(SpokenScene):
    def construct(self):
        pair = microscope_pair()
        self.add(pair)
        self.at("appearance has reached")
        stop = VGroup(Line([-1.8, .25, 0], [1.8, .25, 0], color=RED, stroke_width=14),
                      T("LOOKS", 34, RED, weight=BOLD).move_to([0, .75, 0]))
        stop[1].layout_ok = True
        self.play(FadeIn(stop), run_time=.7)
        self.at("key must change evidence")
        strips = sequence_strips()
        self.play(FadeOut(VGroup(pair, stop)), FadeIn(strips.labels), run_time=.8)
        self.at("Ribosomal RNA")
        title = T("ribosomal RNA", 38, TEXT, weight=BOLD).move_to([0, 2.75, 0])
        self.play(Write(title), run_time=.8)
        self.at("Every cell uses")
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * .12) for x in strips.blue], lag_ratio=.08), run_time=1.3)
        self.at("build proteins")
        protein = evidence_block("protein", TEXT, 2.2).move_to([0, -2.25, 0])
        self.play(FadeIn(protein, shift=UP * .2), run_time=.7)
        self.at("sequence patterns differ")
        self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * .12) for x in strips.teal], lag_ratio=.08),
                  FadeIn(strips.tag), run_time=1.3)
        self.at("Bacteria and Archaea")
        diffs = VGroup(*[strips.blue[i] for i in DIFFS], *[strips.teal[i] for i in DIFFS])
        self.play(LaggedStart(*[Indicate(x, scale_factor=1.12) for x in diffs], lag_ratio=.12), run_time=1.5)
        self.finish()


class S07Compare(SpokenScene):
    def construct(self):
        strips = sequence_strips()
        self.add(strips)
        bob(strips.blue, amp=.075, speed=.65)
        bob(strips.teal, amp=.075, speed=.72, seed=2)
        self.at("labelled strip")
        self.play(Indicate(strips.blue, color=BLUE), Indicate(strips.teal, color=TEAL), run_time=1.1)
        self.at("Matching positions")
        matches = [i for i in range(len(SEQ)) if i not in DIFFS]
        locks = VGroup(*[Line(strips.blue[i].get_bottom(), strips.teal[i].get_top(),
                             color=TEXT, stroke_width=4) for i in matches])
        self.play(LaggedStart(*[Create(x) for x in locks], lag_ratio=.08), run_time=1.2)
        scan = Line([0, strips.blue.get_top()[1] + .15, 0], [0, strips.teal.get_bottom()[1] - .15, 0],
                    color=TEXT, stroke_width=5)
        scan.layout_ok = True
        x0, x1 = strips.blue.get_left()[0], strips.blue.get_right()[0]
        scan._t = 0.0

        def _scan(m, dt):
            m._t += dt
            m.move_to([x0 + (x1 - x0) * (0.5 + 0.5 * np.sin(1.1 * m._t - 1.57)), m.get_center()[1], 0])
        scan.add_updater(_scan)
        self.add(scan)
        self.at("differences flash")
        diffs = VGroup(*[strips.blue[i] for i in DIFFS], *[strips.teal[i] for i in DIFFS])
        self.play(LaggedStart(*[Indicate(x, scale_factor=1.13) for x in diffs], lag_ratio=.12), run_time=1.3)
        self.at("judge relatedness")
        brace = Brace(VGroup(strips.blue, strips.teal), RIGHT, color=TEXT)
        related = VGroup(T("compare", 28, TEXT), T("patterns", 28, TEXT)).arrange(DOWN, buff=.08)
        related.move_to([5.45, .05, 0])
        self.play(GrowFromCenter(brace), FadeIn(related), run_time=.8)
        bob(related, amp=.05, speed=.7, seed=3)
        self.at("methane making microbes")
        scan.clear_updaters()
        self.remove(scan)
        self.play(FadeOut(VGroup(locks, brace, related)), run_time=.5)
        paths = VGroup(
            VMobject(color=BLUE, stroke_width=8).set_points_smoothly([[-.2, -.2, 0], [-2.0, -1.5, 0], [-4.1, -2.4, 0]]),
            VMobject(color=TEAL, stroke_width=8).set_points_smoothly([[.2, -.2, 0], [2.0, -1.5, 0], [4.1, -2.4, 0]]))
        small_b = sequence_strips().blue.scale(.6).move_to([-3.8, .7, 0])
        small_a = sequence_strips().teal.scale(.6).move_to([3.8, .7, 0])
        self.play(FadeOut(VGroup(strips.blue, strips.teal, strips.labels, strips.tag)),
                  FadeIn(small_b), FadeIn(small_a), Create(paths), run_time=1.3)
        self.at("typical bacteria")
        cells = VGroup(mystery_cell(BLUE, [-4.1, -2.35, 0], .46, dna=False),
                       mystery_cell(TEAL, [4.1, -2.35, 0], .46, dna=False))
        self.play(FadeIn(cells), run_time=.7)
        self.at("molecules still differed")
        self.play(ShowPassingFlash(paths.copy().set_stroke(TEXT, 13), time_width=.5), run_time=1.5)
        self.finish()


class S08Chemistry(SpokenScene):
    def construct(self):
        world = chemistry_panels()
        bob(world.cells[0], amp=.075, speed=.7)
        bob(world.cells[1], amp=.075, speed=.78, seed=2)
        self.play(FadeIn(world.panels), FadeIn(world.cells), run_time=.9)
        self.at("Cell chemistry")
        self.play(Indicate(world.cells, color=TEXT), run_time=.8)
        self.at("Most bacteria have peptidoglycan")
        self.play(FadeIn(world.wall_blocks[0], shift=UP * .15), run_time=.8)
        self.at("Archaeal walls have none")
        self.play(FadeIn(world.wall_blocks[1], shift=UP * .15), run_time=.8)
        self.at("membrane lipid")
        heads = VGroup(*[RoundedRectangle(corner_radius=.08, width=.65, height=.38,
                                          color=c, fill_color=c, fill_opacity=.25)
                         for c in (BLUE, TEAL)]).arrange(RIGHT, buff=5.95).move_to([0, -1.02, 0])
        tails = VGroup(*[VGroup(Line(h.get_bottom() + LEFT * .16, h.get_bottom() + DOWN * .52 + LEFT * .16,
                                         color=c, stroke_width=5),
                                  Line(h.get_bottom() + RIGHT * .16, h.get_bottom() + DOWN * .52 + RIGHT * .16,
                                         color=c, stroke_width=5)) for h, c in zip(heads, (BLUE, TEAL))])
        self.play(FadeIn(heads), Create(tails), run_time=.8)
        self.at("chemical link holds")
        links = VGroup(T("link", 26, BLUE).next_to(tails[0], DOWN, buff=.1),
                       T("link", 26, TEAL).next_to(tails[1], DOWN, buff=.1))
        self.play(FadeIn(links), run_time=.6)
        self.at("Typical bacteria use ester")
        self.play(FadeOut(VGroup(heads, tails, links)), FadeIn(world.link_blocks[0]), run_time=.8)
        self.at("typical archaea use ether")
        self.play(FadeIn(world.link_blocks[1]), run_time=.8)
        self.at("No single sketch")
        self.play(Indicate(world.wall_blocks), Indicate(world.link_blocks), run_time=1.0)
        self.at("full pattern of evidence")
        cap = caption("Use the full pattern of evidence.", 34, TEXT)
        self.play(FadeIn(cap, shift=UP * .15), run_time=.8)
        self.finish()


class S09Place(SpokenScene):
    def construct(self):
        cell = mystery_cell(TEAL, [-4.9, .45, 0], 1.05, dna=True)
        self.add(cell)
        evidence = VGroup(
            evidence_block("archaeal sequence", TEXT, 3.15),
            evidence_block("no peptidoglycan", TEXT, 3.15),
            evidence_block("ether-linked lipids", TEXT, 3.15),
        ).arrange(DOWN, buff=.25).move_to([-.9, .45, 0])
        self.at("archaeal sequence pattern")
        self.play(FadeIn(evidence[0], shift=LEFT * .2), run_time=.7)
        self.at("no peptidoglycan")
        self.play(FadeIn(evidence[1], shift=LEFT * .2), run_time=.7)
        self.at("ether linked membrane lipids")
        self.play(FadeIn(evidence[2], shift=LEFT * .2), run_time=.7)
        self.at("Together those traits")
        self.play(evidence.animate.arrange(RIGHT, buff=.12).scale(.72).move_to([-.3, .45, 0]), run_time=1.0)
        self.at("support Archaea")
        gate = RoundedRectangle(corner_radius=.2, width=2.4, height=4.4, color=TEAL,
                                stroke_width=8).move_to([5.25, .45, 0])
        gate_lab = T("Archaea", 34, TEAL, weight=BOLD).next_to(gate, UP, buff=.18)
        self.play(Create(gate), FadeIn(gate_lab), run_time=.8)
        pulse(gate, base=8, amp=1.6, speed=1.25)
        self.at("different pattern")
        alt = Arrow([3.25, -2.0, 0], [5.85, -2.0, 0], color=BLUE, stroke_width=5, tip_length=.25)
        alt_lab = T("Bacteria", 28, BLUE).next_to(alt, DOWN, buff=.12)
        self.play(GrowArrow(alt), FadeIn(alt_lab), run_time=.7)
        self.at("gate opens only")
        door = Line(gate.get_top(), gate.get_bottom(), color=TEAL, stroke_width=10)
        self.add(door)
        self.play(Rotate(door, angle=-PI / 2, about_point=door.get_bottom()), run_time=1.0)
        self.at("supports the placement")
        route = VMobject().set_points_smoothly([[-4.9, .45, 0], [-2.8, 2.2, 0], [1.5, 2.3, 0], [5.25, .45, 0]])
        self.play(MoveAlongPath(cell, route), evidence.animate.move_to([.45, .45, 0]), run_time=1.8)
        self.finish()


class S10Tree(SpokenScene):
    def construct(self):
        stair = VGroup(*[Line([-5 + i * 1.45, -2.4 + i * .9, 0],
                                  [-3.55 + i * 1.45, -2.4 + i * .9, 0],
                                  color=RED, stroke_width=7) for i in range(5)])
        self.play(Create(stair), run_time=.8)
        self.at("branches, not steps")
        tree = domain_tree()
        self.play(FadeOut(stair), Create(tree.branches), run_time=1.2)
        travellers = VGroup(travel_dot(tree.branches[1], BLUE, .075),
                            travel_dot(tree.branches[3], TEAL, .085, .33),
                            travel_dot(tree.branches[4], GOLD, .08, .66))
        self.add(travellers)
        self.at("show relatedness")
        self.play(FadeIn(tree.labels), run_time=.8)
        self.at("not a ladder")
        ghost_stair = stair.copy().set_opacity(.25)
        cross = Cross(ghost_stair, stroke_color=RED, stroke_width=8)
        self.play(FadeIn(ghost_stair), Create(cross), run_time=.8)
        self.play(FadeOut(VGroup(ghost_stair, cross)), run_time=.4)
        self.at("All branches share a root")
        self.play(FadeIn(tree.root_label), Indicate(tree.branches[0], color=TEXT), run_time=.8)
        self.at("drawing is simplified")
        self.play(FadeIn(tree.tag), run_time=.6)
        self.at("Archaea and Eukarya")
        self.play(ShowPassingFlash(VGroup(tree.branches[2].copy(), tree.branches[3].copy(),
                                          tree.branches[4].copy()).set_stroke(TEXT, 13), time_width=.6), run_time=1.4)
        self.at("closely related")
        self.play(Indicate(VGroup(tree.labels[1], tree.labels[2]), color=TEXT, scale_factor=1.08), run_time=1.0)
        self.at("either is to bacteria")
        self.play(Indicate(tree.labels[0], color=BLUE), run_time=.8)
        self.finish()


class S11Limit(SpokenScene):
    def construct(self):
        path = ordered_path()
        self.play(FadeIn(path[0][0]), run_time=.5)
        pulse(path[0][0][0], base=4, amp=1.2, speed=1.2)
        self.at("path has a limit")
        self.play(LaggedStart(*[GrowArrow(a) for a in path[1]],
                              *[FadeIn(n) for n in path[0][1:]], lag_ratio=.12), run_time=1.3)
        self.at("domain scheme")
        domains = VGroup(T("Bacteria", 30, BLUE), T("Archaea", 30, TEAL), T("Eukarya", 30, GOLD)).arrange(RIGHT, buff=.7)
        domains.move_to([0, -1.45, 0])
        self.play(FadeIn(domains), run_time=.7)
        self.at("does not identify every species")
        stop = RegularPolygon(8, radius=.65, color=RED, stroke_width=6,
                              fill_color=RED, fill_opacity=.18).move_to([5.2, -2.35, 0])
        stop_lab = T("SPECIES", 25, RED, weight=BOLD).move_to(stop)
        stop_lab.layout_ok = True
        self.play(FadeIn(stop), FadeIn(stop_lab), run_time=.8)
        self.at("Keep the method")
        self.play(FadeOut(domains), FadeOut(VGroup(stop, stop_lab)),
                  ShowPassingFlash(path.copy().set_color(TEXT), time_width=.5), run_time=1.1)
        self.at("Classify by ordered traits")
        rule1 = T("Classify by ordered traits;", 38, TEXT, weight=BOLD).move_to([0, -1.25, 0])
        self.play(Write(rule1), run_time=.9)
        self.at("Where looks fail")
        self.play(Indicate(path[0][2], color=RED), run_time=.7)
        self.at("use molecular evidence")
        rule2 = T("where looks fail, use molecular evidence.", 38, TEAL, weight=BOLD).next_to(rule1, DOWN, buff=.25)
        fit(rule2, max_w=11.8)
        self.play(Write(rule2), Indicate(path[0][3], color=TEAL), run_time=1.0)
        self.finish()


class S12End(EndCard):
    LINE = "Classify by ordered traits; where looks fail, use molecular evidence."
