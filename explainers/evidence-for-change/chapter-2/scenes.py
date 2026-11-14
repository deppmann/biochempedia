"""Two Clues, One Family Tree — one carried family-tree world.

COLOUR MAP (identical to chapter 1)
    GOLD   fossils and fossil-bearing observations
    BLUE   matching body structures
    TEAL   DNA and protein sequences
    GREEN  supported comparisons and inferences
    GREY   missing or uncertain evidence

Every tree and carried clue is rebuilt by the builders below at fixed coordinates.  All diagrams
are explicitly schematic; no molecular structure or quantitative molecular clock is drawn.
"""
from bp_parts import *


ROCK = "#6F5A49"
ROCK_LIGHT = "#92765C"
WATER = "#367A96"
SAND = "#B99A68"


# Carry a quiet strip of the chapter-1 riverbank beneath every spoken scene.  Besides keeping the
# pair visually continuous, the falling grains prevent a narrated hold from becoming a dead frame.
_spoken_setup = SpokenScene.setup


def _living_setup(self):
    _spoken_setup(self)
    ground = Rectangle(width=14.2, height=1.65, stroke_width=0, fill_color=ROCK,
                       fill_opacity=0.36).move_to([0, -3.18, 0])
    top = Line([-7.1, -2.36, 0], [7.1, -2.36, 0], color=SAND, stroke_width=3).set_opacity(0.65)
    rng = np.random.default_rng(sum(map(ord, os.environ.get("KX_SCENE_ID", "scene"))))
    grains = VGroup(*[Dot([rng.uniform(-6.8, 6.8), rng.uniform(-3.72, -2.42), 0],
                              radius=rng.uniform(0.065, 0.110), color=SAND).set_opacity(0.65)
                       for _ in range(64)])
    grains._phase = 0.0

    def flow(mob, dt):
        mob._phase += dt
        for i, dot in enumerate(mob):
            dot.shift(RIGHT * (0.78 + 0.045 * (i % 5)) * dt)
            if dot.get_x() > 7.0:
                dot.shift(LEFT * 14.0)
    grains.add_updater(flow)
    self.add(ground, top, grains)


SpokenScene.setup = _living_setup


def drift(mob, dx=0.05, dy=0.0, span=0.35):
    """Small continuous motion, kept local so the carried layout does not migrate."""
    mob._origin = mob.get_center().copy()
    mob._phase = 0.0

    def update(m, dt):
        m._phase += dt
        target = m._origin + np.array([dx * np.sin(m._phase), dy * np.sin(0.7 * m._phase), 0])
        m.shift(target - m.get_center())
    mob.add_updater(update)
    return mob


def moving_water(y=2.90, width=3.0, x=-5.45):
    river = Rectangle(width=width, height=0.75, stroke_color=WATER, stroke_width=3,
                      fill_color=WATER, fill_opacity=0.48).move_to([x, y, 0])
    waves = VGroup(*[Line([x - 1.25 + i * 0.65, y + 0.08 * (-1) ** i, 0],
                          [x - 0.85 + i * 0.65, y + 0.08 * (-1) ** i, 0],
                          color=TEXT, stroke_width=2).set_opacity(0.50) for i in range(4)])
    waves._phase = 0.0

    def flow(m, dt):
        m._phase += dt
        m.shift(RIGHT * 0.12 * dt)
        if m.get_left()[0] > x - 1.05:
            m.shift(LEFT * 0.65)
    waves.add_updater(flow)
    return VGroup(river, waves)


def fossil_bank_edge():
    """Chapter 1's riverbank compressed at the left edge, at stable coordinates."""
    layers = VGroup(*[
        Rectangle(width=2.8 - i * 0.08, height=0.42, stroke_color=SAND, stroke_width=1.5,
                  fill_color=c, fill_opacity=0.65).move_to([-5.45, -2.55 + i * 0.45, 0])
        for i, c in enumerate((ROCK, ROCK_LIGHT, ROCK, ROCK_LIGHT, ROCK, ROCK_LIGHT))
    ])
    fossils = VGroup(*[
        Sector(radius=0.23, start_angle=35 * DEGREES, angle=110 * DEGREES,
               stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.3,
               arc_center=np.array(p))
        for p in ([-5.75, -2.58, 0], [-5.15, -1.70, 0], [-5.62, -0.80, 0])
    ])
    grains = VGroup(*[Dot([-6.3 + (i % 5) * 0.42, -2.75 + (i % 4) * 0.55, 0],
                         radius=0.025, color=SAND).set_opacity(0.45) for i in range(12)])
    drift(grains, dx=0.025, dy=-0.025)
    return VGroup(layers, fossils, moving_water(), grains)


def family_tree(color=GREY, labels=(), scale=1.0, at=(0.8, -0.15, 0), questions=False):
    """The film's carried tree: root, one early branch, and a recent sister pair."""
    x, y, _ = at
    root = Line([x, y - 2.40, 0], [x, y - 0.70, 0], color=color, stroke_width=8)
    early = Line([x, y - 1.45, 0], [x - 2.35, y + 1.65, 0], color=color, stroke_width=8)
    stem = Line([x, y - 0.70, 0], [x + 0.45, y + 0.25, 0], color=color, stroke_width=8)
    left = Line([x + 0.45, y + 0.25, 0], [x - 0.20, y + 2.05, 0], color=color, stroke_width=8)
    right = Line([x + 0.45, y + 0.25, 0], [x + 2.25, y + 1.75, 0], color=color, stroke_width=8)
    lines = VGroup(root, early, stem, left, right).scale(scale, about_point=np.array(at))
    g = VGroup(lines)
    g.lines = lines
    g.root, g.early, g.stem, g.left, g.right = lines
    tips = [lines[1].get_end(), lines[3].get_end(), lines[4].get_end()]
    if labels:
        labs = VGroup(*[T(s, 28, TEXT, weight=BOLD).next_to(p, UP, buff=0.13) for s, p in zip(labels, tips)])
        g.add(labs)
        g.labels = labs
    if questions:
        qs = VGroup(*[T("?", 36, GREY).move_to(p + UP * 0.45) for p in
                      (lines[1].get_center(), lines[2].get_center())])
        drift(qs, dx=0.025, dy=0.025)
        g.add(qs)
        g.questions = qs
    return g


def ancestor_tree(with_labels=False, with_blocks=False):
    tree = family_tree(labels=("group 1", "group 2", "group 3") if with_labels else ())
    ancestor = Dot(tree.stem.get_start(), radius=0.24, color=GREEN)
    ancestor_label = T("common ancestor", 30, GREEN, weight=BOLD).next_to(ancestor, RIGHT, buff=0.25)
    g = VGroup(tree, ancestor, ancestor_label)
    g.tree, g.ancestor, g.ancestor_label = tree, ancestor, ancestor_label
    if with_blocks:
        blocks = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.62, height=0.34,
                                           stroke_color=BLUE, stroke_width=3,
                                           fill_color=BLUE, fill_opacity=0.25).move_to(p)
                          for p in (tree.early.point_from_proportion(0.68),
                                    tree.left.point_from_proportion(0.68),
                                    tree.right.point_from_proportion(0.68))])
        g.add(blocks)
        g.blocks = blocks
    return g


def bone_badge(at=ORIGIN, scale=1.0):
    upper = RoundedRectangle(corner_radius=0.10, width=1.05, height=0.32,
                             stroke_color=BLUE, stroke_width=4, fill_color=BLUE,
                             fill_opacity=0.24)
    ends = VGroup(Dot(LEFT * 0.52, radius=0.18, color=BLUE),
                  Dot(RIGHT * 0.52, radius=0.18, color=BLUE))
    return VGroup(upper, ends).scale(scale).move_to(at)


def protein_strip(text="A  G  L  V  T", at=ORIGIN, width=3.0, color=TEAL):
    box = RoundedRectangle(corner_radius=0.12, width=width, height=0.62,
                           stroke_color=color, stroke_width=3, fill_color=color,
                           fill_opacity=0.12).move_to(at)
    lab = M(text, 25, color).move_to(box)
    lab.layout_ok = True  # deliberate sequence printed inside its strip
    return VGroup(box, lab)


def limb_diagram(name, job, variant=0):
    """A simplified positional block map, not an anatomical reconstruction."""
    upper = RoundedRectangle(corner_radius=0.10, width=0.48, height=1.08 + 0.08 * variant,
                             stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.20)
    lower1 = RoundedRectangle(corner_radius=0.08, width=0.20, height=1.02,
                              stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.20)
    lower2 = lower1.copy()
    lowers = VGroup(lower1, lower2).arrange(RIGHT, buff=0.13).next_to(upper, DOWN, buff=0.10)
    wrist = RoundedRectangle(corner_radius=0.06, width=0.78 + 0.08 * variant, height=0.30,
                             stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.20)
    wrist.next_to(lowers, DOWN, buff=0.10)
    fingers = VGroup(*[Line(ORIGIN, DOWN * (0.48 + 0.08 * ((i + variant) % 2)),
                             color=BLUE, stroke_width=4) for i in range(4)]).arrange(RIGHT, buff=0.13)
    fingers.next_to(wrist, DOWN, buff=0.08)
    parts = VGroup(upper, lowers, wrist, fingers)
    title = T(name, 29, TEXT, weight=BOLD).next_to(parts, UP, buff=0.18)
    job_lab = chip(job, GREY, 28).next_to(parts, DOWN, buff=0.18)
    g = VGroup(parts, title, job_lab)
    g.parts, g.upper, g.lowers, g.wrist, g.fingers, g.job = parts, upper, lowers, wrist, fingers, job_lab
    return g


def four_limbs(with_jobs=True):
    specs = (("human arm", "grasp", 0), ("cat leg", "walk", 1),
             ("whale flipper", "swim", 2), ("bat wing", "fly", 3))
    limbs = VGroup(*[limb_diagram(*s) for s in specs]).arrange(RIGHT, buff=0.62)
    limbs.move_to([0, 0.05, 0])
    if not with_jobs:
        for limb in limbs:
            limb.remove(limb.job)
    return limbs


def aligned_sequences(at=(0, 0, 0), names=("species A", "species B", "species C")):
    rows = (("A  G  L  V  T", names[0]), ("A  G  L  V  T", names[1]), ("A  S  L  I  T", names[2]))
    strips = VGroup()
    for seq, name in rows:
        strip = protein_strip(seq, width=4.0)
        label = T(name, 27, TEXT).next_to(strip, LEFT, buff=0.25)
        strips.add(VGroup(label, strip))
    strips.arrange(DOWN, aligned_edge=RIGHT, buff=0.24).move_to(at)
    return strips


def case_world(pair=(0, 1), structure_pair=(0, 1), question=False, green=False,
               names=("species A", "species B", "species C")):
    tree = family_tree(color=GREY, labels=names, scale=0.92, at=(0, -0.15, 0))
    tips = [tree.early.get_end(), tree.left.get_end(), tree.right.get_end()]
    def bracket(indices, col, y):
        xs = [tips[i][0] for i in indices]
        return VGroup(Line([min(xs), y, 0], [max(xs), y, 0], color=col, stroke_width=6),
                      Line([min(xs), y, 0], [min(xs), y - 0.25, 0], color=col, stroke_width=6),
                      Line([max(xs), y, 0], [max(xs), y - 0.25, 0], color=col, stroke_width=6))
    blue = bracket(structure_pair, BLUE, 2.75)
    teal = bracket(pair, TEAL, 2.30)
    drift(blue, dx=0.018, dy=0.01)
    drift(teal, dx=-0.018, dy=0.01)
    g = VGroup(tree, blue, teal)
    g.tree, g.blue, g.teal = tree, blue, teal
    if green:
        support = SurroundingRectangle(VGroup(*[tree.labels[i] for i in pair]), color=GREEN,
                                       stroke_width=5, buff=0.23)
        g.add(support)
        g.support = support
    if question:
        q = question_card("Do the clues agree?", y=-3.18, max_w=8.0)
        q.question.set_stroke(BG, width=12, opacity=1, background=True)
        g.add(q)
        g.question = q
    return g


class S00LinkQuestion(SpokenScene):
    def construct(self):
        bank = fossil_bank_edge()
        tree = family_tree(at=(1.15, -0.20, 0), scale=1.12, questions=True)
        self.add(bank)
        self.play(Create(tree.lines), run_time=1.0)
        self.at("bat wing and a protein")
        bone = bone_badge([-2.0, 1.30, 0], 1.15)
        seq = protein_strip("A  G  L  V", [4.65, 0.50, 0], width=2.9)
        self.play(FadeIn(bone, shift=RIGHT * 0.2), FadeIn(seq, shift=LEFT * 0.2), run_time=0.65)
        self.at("first film used fossils")
        self.play(bank.animate.shift(LEFT * 0.30), Indicate(bank[1], color=GOLD, scale_factor=1.04), run_time=0.7)
        self.at("test relationships")
        q = T("Which branches are closest?", 40, TEXT, weight=BOLD).move_to([1.15, -3.25, 0])
        self.play(FadeIn(q, shift=UP * 0.12), tree.animate.scale(1.03), run_time=0.55)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Evidence for Change"
    TITLE = "Two Clues, One Family Tree"

    def construct(self):
        tree = family_tree(at=(1.0, -0.1, 0), scale=1.05, questions=False)
        bank = fossil_bank_edge()
        bone = bone_badge([-3.25, 1.55, 0], 0.9)
        seq = protein_strip("A  G  L  V", [4.65, 1.35, 0], width=2.6)
        drift(seq, dx=0.035)
        veil = Rectangle(width=12.4, height=2.0, stroke_width=0, fill_color=BG,
                         fill_opacity=0.80).move_to([0, 0.1, 0])
        title = T(self.TITLE, 50, TEXT, font=TITLE_FONT).move_to([0, 0.12, 0])
        lesson = T(self.LESSON.upper(), 24, TEAL, weight=BOLD).move_to([0, 0.78, 0])
        rule = Line(LEFT * 1.4, RIGHT * 1.4, color=GOLD, stroke_width=4).move_to([0, -0.46, 0])
        self.add(bank, tree, bone, seq)
        self.play(FadeIn(veil), FadeIn(lesson), Write(title), GrowFromCenter(rule), run_time=1.0)
        self.finish()


class S02CommonAncestor(SpokenScene):
    def construct(self):
        trunk = family_tree(at=(0, -0.15, 0), scale=1.15)
        # Show the growing branch before naming its split.
        self.play(Create(trunk.root), run_time=0.55)
        self.play(Create(VGroup(trunk.early, trunk.stem, trunk.left, trunk.right)), run_time=1.1)
        self.at("common ancestor is")
        ancestor = Dot(trunk.stem.get_start(), radius=0.25, color=GREEN)
        label = T("common ancestor", 32, GREEN, weight=BOLD).next_to(ancestor, RIGHT, buff=0.25)
        self.play(GrowFromCenter(ancestor), FadeIn(label, shift=LEFT * 0.15), run_time=0.6)
        self.at("one branch splitting")
        self.play(Indicate(VGroup(trunk.stem, trunk.left, trunk.right), color=GREEN, scale_factor=1.02), run_time=0.65)
        self.at("inherits old features")
        block0 = bone_badge(ancestor.get_center() + UP * 0.25, 0.50)
        targets = [bone_badge(trunk.early.point_from_proportion(0.72), 0.50),
                   bone_badge(trunk.left.point_from_proportion(0.72), 0.50),
                   bone_badge(trunk.right.point_from_proportion(0.72), 0.50)]
        self.play(FadeIn(block0), run_time=0.35)
        copies = VGroup(*[block0.copy() for _ in targets])
        self.add(copies)
        self.play(*[Transform(c, t) for c, t in zip(copies, targets)], FadeOut(block0), run_time=1.0)
        self.at("changes in its own direction")
        self.play(copies[0].animate.stretch(1.35, 0).rotate(-0.25),
                  copies[1].animate.stretch(1.30, 1).rotate(0.15),
                  copies[2].animate.stretch(1.45, 0).rotate(0.35), run_time=0.8)
        self.add(scope_tag("schematic"))
        self.finish()


class S03BoneMap(SpokenScene):
    def construct(self):
        limbs = four_limbs(True)
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.15) for x in limbs], lag_ratio=0.16), run_time=1.0)
        self.at("upper bone")
        upper_line = Line([-5.8, 1.05, 0], [5.8, 1.05, 0], color=BLUE, stroke_width=4)
        upper_lab = T("upper bone", 28, BLUE).move_to([0, 3.28, 0])
        self.play(Create(upper_line), FadeIn(upper_lab), run_time=0.6)
        self.at("paired lower bones")
        lower_line = Line([-5.8, 0.0, 0], [5.8, 0.0, 0], color=BLUE, stroke_width=4)
        lower_lab = T("paired lower bones", 28, BLUE).move_to([0, 3.28, 0])
        self.play(Transform(upper_line, lower_line), swap(upper_lab, lower_lab), run_time=0.65)
        self.at("Wrist and finger bones")
        end_line = Line([-5.8, -1.23, 0], [5.8, -1.23, 0], color=BLUE, stroke_width=4)
        end_lab = T("wrist + fingers", 28, BLUE).move_to([0, 3.28, 0])
        self.play(Transform(upper_line, end_line), swap(lower_lab, end_lab), run_time=0.65)
        self.at("Shapes and jobs differ")
        self.play(LaggedStart(*[Indicate(x.job, color=GREY, scale_factor=1.05) for x in limbs], lag_ratio=0.12), run_time=0.8)
        self.at("positions match")
        self.play(FadeOut(end_lab), Indicate(VGroup(*[x.parts for x in limbs]), color=BLUE, scale_factor=1.02), run_time=0.8)
        self.finish()


class S04Construction(SpokenScene):
    def construct(self):
        limbs = four_limbs(True)
        self.add(limbs)
        self.at("construction and position")
        jobs = VGroup(*[x.job for x in limbs])
        self.play(FadeOut(jobs, shift=DOWN * 0.45), run_time=0.7)
        guides = VGroup(*[Line([-5.7, y, 0], [5.7, y, 0], color=BLUE, stroke_width=3).set_opacity(0.65)
                          for y in (1.05, 0.0, -0.72, -1.28)])
        self.play(LaggedStart(*[Create(g) for g in guides], lag_ratio=0.14), run_time=0.8)
        self.at("reshape an old set")
        self.play(*[limb.parts.animate.stretch(1.0 + i * 0.07, 0) for i, limb in enumerate(limbs)], run_time=0.75)
        self.at("shared bone map")
        tree = family_tree(at=(3.7, -0.45, 0), scale=0.62)
        ancestor = Dot(tree.stem.get_start(), radius=0.18, color=GREEN)
        tag = chip("same construction + position", GREEN, 27).move_to([-2.65, -1.92, 0])
        same_job = chip("same job?", GREY, 26).move_to([-4.75, 2.55, 0])
        self.play(FadeOut(guides), FadeOut(limbs, shift=LEFT * 0.8), FadeIn(tree), GrowFromCenter(ancestor),
                  FadeIn(same_job), run_time=0.8)
        self.play(same_job.animate.shift(LEFT * 2.0).set_opacity(0.15), FadeIn(tag), run_time=0.7)
        self.at("common ancestor")
        links = VGroup(Arrow(tag.get_right(), ancestor.get_left(), color=GREEN, buff=0.12,
                             stroke_width=4, tip_length=0.17),
                       Arrow(tree.left.get_end(), ancestor.get_center(), color=BLUE, buff=0.15,
                             stroke_width=3, tip_length=0.14),
                       Arrow(tree.right.get_end(), ancestor.get_center(), color=BLUE, buff=0.15,
                             stroke_width=3, tip_length=0.14))
        self.play(LaggedStart(*[GrowArrow(a) for a in links], lag_ratio=0.18), run_time=0.85)
        self.add(scope_tag("schematic"))
        self.finish()


class S05Sequence(SpokenScene):
    def construct(self):
        tree = family_tree(at=(4.55, -0.55, 0), scale=0.54)
        mini_limbs = VGroup(bone_badge(tree.early.get_end(), 0.38), bone_badge(tree.left.get_end(), 0.38),
                            bone_badge(tree.right.get_end(), 0.38))
        self.add(tree, mini_limbs)
        self.at("Sequences offer a test")
        dna = protein_strip("A  T  G  C  A", [-2.8, 1.60, 0], width=4.0)
        dna_lab = T("DNA sequence", 30, TEAL, weight=BOLD).next_to(dna, UP, buff=0.20)
        self.play(FadeIn(dna, shift=RIGHT * 0.2), FadeIn(dna_lab), run_time=0.65)
        self.at("order of its bases")
        cursor = Rectangle(width=0.45, height=0.78, stroke_color=TEXT, stroke_width=3).move_to([-4.15, 1.60, 0])
        self.play(FadeIn(cursor), cursor.animate.shift(RIGHT * 2.7), run_time=1.1, rate_func=linear)
        self.at("instructions for proteins")
        protein = protein_strip("A  G  L  V  T", [-2.8, 1.60, 0], width=4.0)
        protein_lab = T("same protein", 30, TEAL, weight=BOLD).next_to(protein, UP, buff=0.20)
        self.play(ReplacementTransform(dna, protein), swap(dna_lab, protein_lab), FadeOut(cursor), run_time=0.7)
        self.at("same protein from several species")
        rows = aligned_sequences(at=(-2.4, -0.55, 0))
        self.play(Transform(protein, rows[0][1]), FadeOut(protein_lab),
                  FadeIn(rows[0][0]), FadeIn(rows[1]), FadeIn(rows[2]), run_time=0.85)
        self.at("position by position")
        scan = Rectangle(width=0.48, height=2.18, stroke_color=TEXT, stroke_width=3).move_to([-3.65, -0.55, 0])
        self.play(FadeIn(scan), scan.animate.shift(RIGHT * 3.1), run_time=1.5, rate_func=linear)
        self.add(scope_tag("schematic"))
        self.finish()


class S06Changes(SpokenScene):
    def construct(self):
        tree = family_tree(at=(-1.45, -0.2, 0), scale=1.0)
        clock = Circle(radius=0.72, color=GREY, stroke_width=4).move_to([5.15, 1.65, 0])
        hand = Line(clock.get_center(), clock.get_center() + UP * 0.52, color=TEAL, stroke_width=4)
        label = T("schematic", 24, GREY).next_to(clock, DOWN, buff=0.18)
        self.play(Create(tree.lines), FadeIn(clock), FadeIn(hand), FadeIn(label), run_time=0.9)
        self.at("inherited DNA changes")
        ticks = VGroup()
        locs = [(tree.early, .28), (tree.early, .75), (tree.stem, .50),
                (tree.left, .72), (tree.right, .35), (tree.right, .88)]
        for branch, p in locs:
            tick = Line(LEFT * 0.14, RIGHT * 0.14, color=TEAL, stroke_width=6).rotate(0.6).move_to(branch.point_from_proportion(p))
            ticks.add(tick)
        self.play(LaggedStart(*[FadeIn(t, scale=1.4) for t in ticks[:3]], lag_ratio=0.25),
                  Rotate(hand, angle=-1.7, about_point=clock.get_center()), run_time=1.2)
        self.at("Branches split at different times")
        self.play(Indicate(VGroup(tree.stem, tree.left, tree.right), color=TEAL, scale_factor=1.02),
                  Rotate(hand, angle=-1.2, about_point=clock.get_center()), run_time=0.8)
        self.at("more similar sequences")
        near = VGroup(protein_strip("A G L V", [3.8, -0.45, 0], width=2.8),
                      protein_strip("A G L V", [3.8, -1.18, 0], width=2.8))
        early = protein_strip("A S L I", [3.8, -2.12, 0], width=2.8)
        self.play(FadeIn(near), FadeIn(early), LaggedStart(*[FadeIn(t) for t in ticks[3:]], lag_ratio=0.25), run_time=1.0)
        self.at("Usually matters")
        ruler = VGroup(Line([4.0, 2.90, 0], [6.1, 2.90, 0], color=GREY, stroke_width=5),
                       T("fixed rate", 26, GREY).move_to([5.05, 3.25, 0]))
        self.play(FadeIn(ruler), Rotate(hand, angle=0.25, about_point=clock.get_center(), rate_func=wiggle), run_time=0.8)
        self.at("not build up at one steady rate")
        self.play(FadeOut(ruler, shift=RIGHT * 0.4), Rotate(hand, angle=-1.0, about_point=clock.get_center()), run_time=0.9)
        self.finish()


class S07Predict(SpokenScene):
    def construct(self):
        world = case_world(pair=(0, 2), structure_pair=(0, 1), question=False)
        self.play(Create(world.tree.lines), FadeIn(world.tree.labels), run_time=0.8)
        self.at("share a blue structure")
        blue_lab = T("shared structure; C lacks it", 27, BLUE).move_to([-3.45, 3.28, 0])
        self.play(Create(world.blue), FadeIn(blue_lab), run_time=0.65)
        self.at("teal protein strip")
        teal_lab = T("matching protein strip", 27, TEAL).move_to([3.90, 3.28, 0])
        self.play(Create(world.teal), FadeIn(teal_lab), run_time=0.65)
        self.at("Have the clues agreed")
        q = question_card("Do the clues agree?", y=-3.18, max_w=8.2)
        q.question.set_stroke(BG, width=12, opacity=1, background=True)
        self.play(FadeIn(q.question, shift=UP * 0.12), run_time=0.55)
        self.at("branch turn green yet")
        self.play(Indicate(world.tree.lines, color=GREY, scale_factor=1.01), run_time=0.65)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "Do the clues agree?"
    OPTIONS = ()
    SECONDS = 4.5
    CARD = {"y": -3.18, "max_w": 8.2}

    def backdrop(self):
        return case_world(pair=(0, 2), structure_pair=(0, 1), question=False)


class S09Conflict(SpokenScene):
    def construct(self):
        world = case_world(pair=(0, 2), structure_pair=(0, 1), question=False)
        self.add(world)
        not_yet = T("Not yet", 44, GREY, weight=BOLD).move_to([0, -3.18, 0])
        not_yet.set_stroke(BG, width=12, opacity=1, background=True)
        self.play(FadeIn(not_yet, scale=1.12), run_time=0.45)
        self.at("different groupings")
        self.play(Indicate(world.blue, color=BLUE, scale_factor=1.03),
                  Indicate(world.teal, color=TEAL, scale_factor=1.03), run_time=0.7)
        self.at("Keep the branches gray")
        self.play(Indicate(world.tree.lines, color=GREY, scale_factor=1.01), run_time=0.6)
        self.at("check the comparison")
        glass = VGroup(Circle(radius=0.48, color=TEXT, stroke_width=5),
                       Line([0.34, -0.34, 0], [0.90, -0.90, 0], color=TEXT, stroke_width=6)).move_to([-3.5, 0.0, 0])
        self.play(FadeIn(glass), glass.animate.shift(RIGHT * 6.5), run_time=1.2)
        self.at("collect more evidence")
        slots = VGroup(*[RoundedRectangle(corner_radius=0.12, width=1.55, height=0.62,
                                          stroke_color=GREY, stroke_width=3).move_to([x, -2.30, 0])
                         for x in (-2.0, 0, 2.0)])
        self.play(FadeOut(glass), FadeOut(not_yet), LaggedStart(*[FadeIn(s) for s in slots], lag_ratio=0.18), run_time=0.75)
        self.at("not something to hide")
        q = T("?", 64, GREY, weight=BOLD).move_to([0, 0.55, 0])
        q.layout_ok = True  # deliberately marks the unresolved split itself
        self.play(FadeIn(q, scale=1.4), run_time=0.55)
        self.at("question to investigate")
        drift(q, dx=0.025, dy=0.035)
        self.play(Indicate(slots, color=GREY, scale_factor=1.04), run_time=0.65)
        self.finish()


class S10Agreement(SpokenScene):
    def construct(self):
        old = case_world(pair=(0, 2), structure_pair=(0, 1), question=False).scale(0.42).move_to([-5.35, 0.0, 0])
        old.tree.remove(old.tree.labels)
        old.set_opacity(0.45)
        self.add(old)
        panel = RoundedRectangle(corner_radius=0.18, width=10.8, height=6.25,
                                 stroke_color=GREY, stroke_width=3).move_to([0.65, 0.0, 0])
        tag = T("a different case", 30, TEXT, weight=BOLD).move_to([0.65, 3.48, 0])
        self.play(FadeIn(panel, shift=LEFT * 0.3), FadeIn(tag), run_time=0.65)
        world = case_world(pair=(0, 1), structure_pair=(0, 1), names=("species D", "species E", "species F"))
        world.scale(0.82).move_to([0.70, -0.15, 0])
        self.at("Two species share a structure")
        self.play(Create(world.tree.lines), FadeIn(world.tree.labels), Create(world.blue), run_time=0.8)
        self.at("protein strip groups that same pair")
        self.play(Create(world.teal), run_time=0.65)
        self.at("independent clues agree")
        # The D/E shared branch is the recent split in this fixed tree.
        self.play(world.tree.stem.animate.set_color(GREEN), world.tree.left.animate.set_color(GREEN),
                  Create(SurroundingRectangle(VGroup(world.tree.labels[0], world.tree.labels[1]),
                                              color=GREEN, stroke_width=5, buff=0.20)), run_time=0.8)
        self.at("stronger explanation")
        support = chip("two clues → one branch", GREEN, 29).move_to([0.7, -2.70, 0])
        self.play(ReplacementTransform(VGroup(world.blue, world.teal), support), run_time=0.75)
        self.finish()


class S11Theory(SpokenScene):
    def construct(self):
        tree = family_tree(at=(0, -0.15, 0), scale=0.82)
        theory = chip("evolution: tested explanation", GREEN, 30).move_to([0, -2.55, 0])
        theory = VGroup(Rectangle(width=theory.width, height=theory.height, stroke_width=0, fill_color=BG,
                                  fill_opacity=0.95).move_to(theory), theory)
        fossil = VGroup(fossil_bank_edge()).scale(0.55).move_to([-4.9, 0.7, 0])
        limb = bone_badge([0, 2.45, 0], 1.05)
        seq = protein_strip("A  G  L  V", [4.85, 0.70, 0], width=2.8)
        self.play(FadeIn(theory), Create(tree.lines), run_time=0.75)
        self.at("Each line of evidence")
        self.play(FadeIn(fossil), FadeIn(limb), FadeIn(seq), run_time=0.7)
        self.at("broad agreement among fossils")
        arrows = VGroup(Arrow(fossil.get_right(), tree.early.get_center(), color=GOLD, buff=0.1, tip_length=0.16),
                        Arrow(limb.get_bottom(), tree.stem.get_center(), color=BLUE, buff=0.1, tip_length=0.16),
                        Arrow(seq.get_left(), tree.right.get_center(), color=TEAL, buff=0.1, tip_length=0.16))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), run_time=1.0)
        self.at("patterns largely agree")
        self.play(Indicate(theory, color=GREEN, scale_factor=1.04), run_time=0.6)
        new = RoundedRectangle(corner_radius=0.12, width=2.6, height=0.85,
                               stroke_color=GREY, stroke_width=3).move_to([4.65, -2.30, 0])
        new_lab = T("new evidence", 27, GREY).move_to(new)
        new_lab.layout_ok = True
        test = Arrow(theory.get_right(), new.get_left(), color=GREEN, stroke_width=4, tip_length=0.16, buff=0.12)
        self.play(FadeIn(new), FadeIn(new_lab), GrowArrow(test), run_time=0.75)
        self.finish()


class S12Limits(SpokenScene):
    def construct(self):
        limb = VGroup(RoundedRectangle(corner_radius=0.15, width=3.0, height=2.0,
                                       stroke_color=GREY, stroke_width=3), bone_badge([0, 0.15, 0], 1.1),
                      T("one clue", 28, GREY).move_to([0, -0.62, 0])).move_to([-2.2, 0.65, 0])
        seq = VGroup(RoundedRectangle(corner_radius=0.15, width=3.0, height=2.0,
                                      stroke_color=GREY, stroke_width=3), protein_strip("A G L V", width=2.5),
                     T("one clue", 28, GREY).move_to([0, -0.62, 0])).move_to([2.2, 0.65, 0])
        self.play(FadeIn(limb), FadeIn(seq), run_time=0.75)
        self.at("cannot settle every relationship")
        qs = VGroup(T("?", 54, GREY).move_to([-2.2, 2.45, 0]), T("?", 54, GREY).move_to([2.2, 2.45, 0]))
        self.play(FadeIn(qs, scale=1.3), run_time=0.6)
        self.at("Similar jobs")
        jobs = VGroup(chip("fly", GREY, 27), chip("fly", GREY, 27)).arrange(RIGHT, buff=2.8).move_to([0, -1.15, 0])
        self.play(FadeIn(jobs), run_time=0.55)
        self.at("different structures")
        self.play(jobs[0].animate.set_color(BLUE), jobs[1].animate.set_color(GREY).rotate(0.18), run_time=0.6)
        self.at("more body parts")
        decks = VGroup(chip("more body parts", BLUE, 30), chip("more sequences", TEAL, 30),
                       chip("fossil record", GOLD, 30)).arrange(DOWN, buff=0.42).move_to([0, 0, 0])
        self.play(FadeOut(VGroup(limb, seq, qs, jobs)), FadeIn(decks[0], shift=UP * 0.15), run_time=0.65)
        self.at("more sequences")
        self.play(FadeIn(decks[1], shift=UP * 0.15), run_time=0.5)
        self.at("fossil record")
        self.play(FadeIn(decks[2], shift=UP * 0.15), run_time=0.5)
        frame = SurroundingRectangle(decks, color=GREY, stroke_width=3, buff=0.35)
        self.play(Create(frame), run_time=0.55)
        self.add(scope_tag("schematic"))
        self.finish()


class S13Return(SpokenScene):
    def construct(self):
        bank = fossil_bank_edge()
        tree = ancestor_tree(with_labels=False, with_blocks=False)
        tree.ancestor_label.move_to([3.25, -1.72, 0])
        self.add(bank)
        self.play(Create(tree.tree.lines), GrowFromCenter(tree.ancestor), FadeIn(tree.ancestor_label), run_time=0.9)
        self.at("Matching parts")
        bones = VGroup(bone_badge(tree.tree.left.get_end(), 0.48), bone_badge(tree.tree.right.get_end(), 0.48))
        self.play(FadeIn(bones), run_time=0.5)
        self.play(*[b.animate.move_to(tree.ancestor.get_center() + offset) for b, offset in zip(bones, (LEFT * .25, RIGHT * .25))], run_time=1.0)
        self.at("Similar sequences")
        strips = VGroup(protein_strip("A G L V", [-0.7, 2.50, 0], width=2.7),
                        protein_strip("A G L V", [2.3, 2.50, 0], width=2.7))
        self.play(FadeIn(strips, shift=DOWN * 0.15), run_time=0.65)
        self.at("independent check")
        scan = Rectangle(width=0.38, height=1.35, stroke_color=TEAL, stroke_width=4).move_to([-1.65, 2.50, 0])
        self.play(FadeIn(scan), scan.animate.shift(RIGHT * 4.9), run_time=1.3, rate_func=linear)
        self.at("both fit one branch pattern")
        blue_link = Arrow(tree.tree.left.get_end(), tree.ancestor.get_center(), color=BLUE, buff=0.15, tip_length=0.16)
        teal_link = Arrow(tree.tree.right.get_end(), tree.ancestor.get_center(), color=TEAL, buff=0.15, tip_length=0.16)
        self.play(GrowArrow(blue_link), GrowArrow(teal_link), tree.tree.stem.animate.set_color(GREEN), run_time=0.85)
        self.at("common ancestry explains")
        self.play(Indicate(tree.ancestor, color=GREEN, scale_factor=1.35), Indicate(bank, color=GOLD, scale_factor=1.01), run_time=0.75)
        self.finish()


class S14Scope(SpokenScene):
    def construct(self):
        tree = family_tree(at=(0, -0.25, 0), scale=0.78, questions=True)
        for mark in tree.questions:
            mark.layout_ok = True  # question marks intentionally sit on unresolved splits
        self.add(tree)
        self.at("clues do different jobs")
        time = chip("time", GOLD, 34).move_to([-4.55, 1.75, 0])
        structure = chip("structure", BLUE, 34).move_to([-4.55, 0.05, 0])
        sequence = chip("sequence", TEAL, 34).move_to([-4.55, -1.65, 0])
        self.play(LaggedStart(FadeIn(time), FadeIn(structure), FadeIn(sequence), lag_ratio=0.18), run_time=0.85)
        self.at("Fossils place life in time")
        gold_link = Arrow(time.get_right(), tree.root.get_start(), color=GOLD, buff=0.12, tip_length=0.16)
        self.play(GrowArrow(gold_link), run_time=0.6)
        self.at("Bones of living and fossil animals")
        blue_link = Arrow(structure.get_right(), tree.left.get_center(), color=BLUE, buff=0.12, tip_length=0.16)
        self.play(GrowArrow(blue_link), run_time=0.6)
        self.at("plus sequences")
        teal_link = Arrow(sequence.get_right(), tree.right.get_center(), color=TEAL, buff=0.12, tip_length=0.16)
        self.play(GrowArrow(teal_link), run_time=0.6)
        self.at("broad agreement supports evolution")
        self.play(tree.stem.animate.set_color(GREEN), tree.left.animate.set_color(GREEN),
                  tree.right.animate.set_color(GREEN), run_time=0.8)
        self.at("uncertainty stays visible")
        self.play(Indicate(tree.questions, color=GREY, scale_factor=1.10), run_time=0.75)
        veil = Rectangle(width=13.2, height=7.2, stroke_width=0, fill_color=BG, fill_opacity=0.20)
        self.play(FadeIn(veil), run_time=0.65)
        self.finish()


class S15End(EndCard):
    LINE = "Matching structures and protein sequences point to common ancestry."
