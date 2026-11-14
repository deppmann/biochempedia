"""Four Tests of Whale Ancestry — evidence-for-evolution, chapter 2.

COLOR MAP (continued throughout this chapter)
  GREY  = rock layers
  GOLD  = fossils and fossil time
  RED   = volcanic ash / a rejected ancestor arrow
  BLUE  = DNA
  GREEN = anatomy
  TEAL  = development
  TEXT  = the branching tree

The tree is always rebuilt by evidence_tree(), so its fork and tips never drift.
"""
from bp_parts import *  # noqa: F401,F403


TIP_Y = 2.45
FORK = np.array([-0.65, -0.35, 0.0])
ROOT = np.array([-0.65, -2.15, 0.0])
WHALE_TIP = np.array([-4.55, TIP_Y, 0.0])
HIPPO_TIP = np.array([0.15, TIP_Y, 0.0])
FISH_TIP = np.array([4.55, TIP_Y, 0.0])


class EvidenceScene(SpokenScene):
    """Spoken scene on the same breathing evidence field.

    The field is a stylistic ground, not a data shape, so layout checking ignores it.
    Its slow luminance cycle prevents long dead holds without moving any landmark.
    """
    def setup(self):
        super().setup()
        field = RoundedRectangle(corner_radius=0.32, width=12.65, height=5.75,
                                 stroke_color=GREY, stroke_width=2,
                                 fill_color=GREY, fill_opacity=0.17).set_z_index(-20)
        field.layout_ok = True
        field._field_t = 0.0

        def breathe(mob, dt):
            mob._field_t += dt
            mob.set_fill(GREY, opacity=0.17 + 0.07 * np.sin(3.2 * mob._field_t))

        field.add_updater(breathe)
        self.add(field)


def evidence_tree(labels=True, opacity=1.0):
    """The carried tree: identical coordinates in every scene."""
    trunk = Line(ROOT, FORK, color=TEXT, stroke_width=10)
    fish_fork = np.array([1.65, 0.55, 0.0])
    branches = VGroup(
        Line(FORK, WHALE_TIP, color=TEXT, stroke_width=8),
        Line(FORK, HIPPO_TIP, color=TEXT, stroke_width=8),
        Line(ROOT + UP * 0.5, fish_fork, color=TEXT, stroke_width=8),
        Line(fish_fork, FISH_TIP, color=TEXT, stroke_width=8),
    )
    nodes = VGroup(Dot(FORK, radius=0.14, color=TEXT), Dot(fish_fork, radius=0.12, color=TEXT))
    g = VGroup(trunk, branches, nodes).set_opacity(opacity)
    g.trunk, g.branches, g.nodes = trunk, branches, nodes
    if labels:
        labs = VGroup(
            T("whale", 30, TEXT).next_to(WHALE_TIP, UP, buff=0.16),
            T("hippo", 30, TEXT).next_to(HIPPO_TIP, UP, buff=0.16),
            T("fish", 30, TEXT).next_to(FISH_TIP, UP, buff=0.16),
        ).set_opacity(opacity)
        g.add(labs)
        g.labels = labs
    return g


def fossil_timeline(x=-5.85):
    line = Line([x, -2.25, 0], [x, 2.35, 0], color=GREY, stroke_width=12)
    strata = VGroup(*[
        Line([x - 0.38, y, 0], [x + 0.38, y, 0], color=GREY, stroke_width=5)
        for y in np.linspace(-1.9, 1.95, 6)
    ])
    fossils = VGroup(*[Dot([x, y, 0], radius=0.11, color=GOLD) for y in (-1.45, -0.55, 0.35, 1.25)])
    ash = Line([x - 0.45, -0.1, 0], [x + 0.45, -0.1, 0], color=RED, stroke_width=6)
    return VGroup(line, strata, fossils, ash)


def lane(label, color, y, x0=-5.25, x1=5.3, end="?"):
    ln = Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=7)
    lab = T(label, 30, color, weight=BOLD).next_to(ln.get_start(), LEFT, buff=0.18)
    mark = T(end, 34, color, weight=BOLD).next_to(ln.get_end(), RIGHT, buff=0.16)
    return VGroup(ln, lab, mark)


def insertion_slots():
    slots = VGroup()
    for tip in (WHALE_TIP, HIPPO_TIP, FISH_TIP):
        slots.add(RoundedRectangle(corner_radius=0.06, width=0.34, height=0.52,
                                   stroke_color=BLUE, stroke_width=3).move_to(tip + DOWN * 0.58))
    return slots


def dna_block_row(marker=False, width=5.2):
    blocks = VGroup(*[
        RoundedRectangle(corner_radius=0.04, width=0.48, height=0.46,
                         stroke_color=BLUE, stroke_width=2.5,
                         fill_color=BLUE, fill_opacity=0.35)
        for _ in range(8)
    ]).arrange(RIGHT, buff=0.12)
    if marker:
        blocks[4].set_fill(BLUE, 0.95).set_stroke(BLUE, 5)
    fit(blocks, max_w=width)
    return blocks


def whale_body(color=GREY, at=ORIGIN, scale=1.0):
    """Simple animal silhouette, intentionally not anatomical detail."""
    body = Ellipse(width=7.4, height=2.75, stroke_color=color, stroke_width=5,
                   fill_color=color, fill_opacity=0.09)
    snout = Polygon([3.0, 0.65, 0], [4.25, 0.28, 0], [3.0, -0.05, 0],
                    stroke_color=color, stroke_width=5, fill_color=color, fill_opacity=0.09)
    tail = Polygon([-3.35, 0.05, 0], [-4.35, 0.95, 0], [-4.0, 0.0, 0],
                   [-4.35, -0.85, 0], stroke_color=color, stroke_width=5,
                   fill_color=color, fill_opacity=0.09)
    eye = Dot([2.65, 0.48, 0], radius=0.08, color=TEXT)
    g = VGroup(body, snout, tail, eye).scale(scale).move_to(at)
    return g


def embryo_body(at=ORIGIN, opacity=1.0):
    body = Ellipse(width=5.4, height=2.9, stroke_color=TEAL, stroke_width=5,
                   fill_color=TEAL, fill_opacity=0.10)
    head = Circle(radius=1.0, stroke_color=TEAL, stroke_width=5,
                  fill_color=TEAL, fill_opacity=0.10).move_to([2.25, 0.55, 0])
    tail = ArcBetweenPoints([-2.5, 0.0, 0], [-3.65, 0.8, 0], angle=-0.7,
                            color=TEAL, stroke_width=8)
    g = VGroup(body, head, tail).set_opacity(opacity).move_to(at)
    return g


def evidence_lanes(end="?", y_values=(2.15, 0.75, -0.65, -2.05)):
    return VGroup(
        lane("fossils", GOLD, y_values[0], end=end),
        lane("DNA", BLUE, y_values[1], end=end),
        lane("anatomy", GREEN, y_values[2], end=end),
        lane("development", TEAL, y_values[3], end=end),
    )


class S00Hook(EvidenceScene):
    def construct(self):
        cliff = VGroup(*[
            Rectangle(width=4.8, height=0.82, stroke_color=GREY, stroke_width=3,
                      fill_color=GREY, fill_opacity=0.16).move_to([-2.55, -2.0 + i * 0.82, 0])
            for i in range(6)
        ])
        fossils = VGroup(*[Dot([-2.55, y, 0], radius=0.15, color=GOLD) for y in (-1.15, 0.3, 1.0)])
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.12) for r in cliff], lag_ratio=0.12),
                  FadeIn(fossils), run_time=1.5)
        self.at("fossil whales in time")
        timeline = fossil_timeline(-5.85)
        tree = evidence_tree().scale(0.75).move_to([1.2, 0.25, 0])
        self.play(ReplacementTransform(VGroup(cliff, fossils), timeline),
                  FadeIn(tree, shift=RIGHT * 0.25), run_time=1.4)
        self.at("If that history")
        lanes = VGroup(
            lane("DNA", BLUE, 1.0, x0=-3.5, x1=4.8),
            lane("anatomy", GREEN, -0.05, x0=-3.5, x1=4.8),
            lane("development", TEAL, -1.1, x0=-3.5, x1=4.8),
        )
        self.play(FadeOut(tree), FadeOut(timeline),
                  LaggedStart(*[FadeIn(x, shift=RIGHT * 0.3) for x in lanes], lag_ratio=0.18), run_time=1.7)
        self.at("what should we find")
        self.play(*[Indicate(x[2], color=x[2].get_color(), scale_factor=1.25) for x in lanes], run_time=1.2)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Evidence for evolution"
    TITLE = "Four Tests of Whale Ancestry"

    def construct(self):
        tree = evidence_tree().scale(0.75).move_to([1.2, 0.25, 0]).set_opacity(0.28)
        tree.layout_ok = True  # deliberately visible behind the opaque title plate
        lesson = T(self.LESSON.upper(), 22, GREY).move_to([0, 2.9, 0])
        title = fit_text(self.TITLE, max_w=10.8, size=50, color=TEXT,
                         font=TITLE_FONT, weight=NORMAL).move_to([0, 0.35, 0])
        plate = RoundedRectangle(corner_radius=0.2, width=title.width + 0.7,
                                 height=title.height + 0.45, stroke_width=0,
                                 fill_color=BG, fill_opacity=0.88).move_to(title).set_z_index(1)
        plate.layout_ok = True
        title.set_z_index(2)
        self.play(FadeIn(tree), FadeIn(lesson), FadeIn(plate), Write(title), run_time=0.75)
        lines = VGroup(*[
            Line([-4.9, y, 0], [4.9, y, 0], color=col, stroke_width=6)
            for y, col in zip((2.0, 0.7, -0.6, -1.9), (GOLD, BLUE, GREEN, TEAL))
        ])
        self.play(FadeOut(title), FadeOut(plate), FadeOut(lesson),
                  LaggedStart(*[Create(x) for x in lines], lag_ratio=0.12), run_time=0.75)
        self.finish()


class S02Tree(EvidenceScene):
    def construct(self):
        tree = evidence_tree(labels=False)
        ladder = VGroup(*[
            Line([-5.4 + i * 0.7, -1.9 + i * 0.65, 0], [-4.7 + i * 0.7, -1.9 + i * 0.65, 0],
                 color=GREY, stroke_width=4) for i in range(5)
        ]).set_opacity(0.38)
        self.play(FadeIn(ladder), run_time=0.7)
        self.at("one branching tree")
        self.play(Create(tree.trunk), run_time=0.6)
        self.at("common ancestor")
        ancestor = chip("ancestral population", TEXT, size=28).move_to(ROOT + LEFT * 2.25)
        self.play(FadeIn(ancestor), GrowFromCenter(tree.nodes[0]), run_time=0.8)
        self.at("later species descended")
        self.play(LaggedStart(*[Create(b) for b in tree.branches], lag_ratio=0.18), run_time=1.7)
        self.at("Branches split")
        self.play(FadeOut(ladder), run_time=0.7)
        self.at("Living species")
        labels = VGroup(
            T("whale", 30).next_to(WHALE_TIP, UP, buff=0.16),
            T("hippo", 30).next_to(HIPPO_TIP, UP, buff=0.16),
            T("fish", 30).next_to(FISH_TIP, UP, buff=0.16),
        )
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.12) for x in labels], lag_ratio=0.15), run_time=0.9)
        self.add(scope_tag("schematic"))
        self.finish()


class S03Dna(EvidenceScene):
    def construct(self):
        tree = evidence_tree()
        self.add(tree, scope_tag("schematic DNA blocks"))
        parent = dna_block_row().scale(0.72).move_to(ROOT + UP * 0.1)
        self.at("DNA passes")
        self.play(FadeIn(parent), run_time=0.7)
        self.at("Small copied changes")
        changed = dna_block_row(marker=True).scale(0.72).move_to(FORK + UP * 0.1)
        self.play(TransformFromCopy(parent, changed), run_time=1.1)
        self.at("travel down a branch")
        whale_copy = dna_block_row(marker=True).scale(0.55).move_to(WHALE_TIP + DOWN * 0.62)
        hippo_copy = dna_block_row(marker=True).scale(0.55).move_to(HIPPO_TIP + DOWN * 0.62)
        self.play(TransformFromCopy(changed, whale_copy), TransformFromCopy(changed, hippo_copy), run_time=1.5)
        self.at("Nearby branches")
        near = chip("less time apart", BLUE, size=28).move_to([3.0, -1.7, 0])
        near.layout_ok = True
        self.play(FadeIn(near), run_time=0.8)
        self.at("Matching DNA stretches")
        self.play(Indicate(VGroup(whale_copy, hippo_copy), color=BLUE, scale_factor=1.06), run_time=1.2)
        self.finish()


def predict_world(with_question=True):
    tree = evidence_tree()
    fork_marker = RoundedRectangle(corner_radius=0.05, width=0.32, height=0.54,
                                   stroke_color=BLUE, stroke_width=4, fill_color=BLUE,
                                   fill_opacity=0.75).move_to(FORK + UP * 0.38)
    slots = insertion_slots()
    qmark = T("?", 54, BLUE, weight=BOLD).move_to([5.25, 0.85, 0])
    g = VGroup(tree, fork_marker, slots, qmark)
    if with_question:
        q = question_card("Where should matching markers appear today?",
                          ["whale + hippo", "whale + fish", "all three"],
                          y=-3.18, chips_at=[3.95, -1.25, 0], max_w=6.2, left=-6.25)
        g.add(q)
    return g


class S04Predict(EvidenceScene):
    def construct(self):
        tree = evidence_tree()
        self.add(tree, scope_tag("schematic"))
        marker = RoundedRectangle(corner_radius=0.05, width=0.32, height=0.54,
                                  stroke_color=BLUE, stroke_width=4, fill_color=BLUE,
                                  fill_opacity=0.75).move_to(FORK + UP * 0.38)
        self.at("insertion spread")
        self.play(FadeIn(marker, scale=0.7), run_time=0.8)
        self.at("before they split")
        self.play(Indicate(tree.nodes[0], color=BLUE, scale_factor=1.5), run_time=0.9)
        self.at("Where should matching markers")
        slots = insertion_slots()
        qmark = T("?", 54, BLUE, weight=BOLD).move_to([5.25, 0.85, 0])
        self.play(LaggedStart(*[FadeIn(s) for s in slots], lag_ratio=0.2), FadeIn(qmark), run_time=1.1)
        self.at("Choose whale and hippo")
        q = question_card("Where should matching markers appear today?",
                          ["whale + hippo", "whale + fish", "all three"],
                          y=-3.18, chips_at=[3.95, -1.25, 0], max_w=6.2, left=-6.25)
        self.play(FadeIn(q.chips), FadeIn(q.question), run_time=1.0)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Where should matching markers appear today?"
    OPTIONS = ["whale + hippo", "whale + fish", "all three"]
    CHIPS_AT = [3.95, -1.25, 0]
    CARD = {"y": -3.18, "max_w": 6.2, "left": -6.25}
    RING_AT = (6.0, -3.1, 0)
    SECONDS = 4.5

    def backdrop(self):
        return predict_world(with_question=False)


class S06Reveal(EvidenceScene):
    def construct(self):
        tree = evidence_tree()
        marker = RoundedRectangle(corner_radius=0.05, width=0.32, height=0.54,
                                  stroke_color=BLUE, stroke_width=4, fill_color=BLUE,
                                  fill_opacity=0.75).move_to(FORK + UP * 0.38)
        slots = insertion_slots()
        timeline = fossil_timeline(-5.85).scale(0.65).shift(DOWN * 0.1)
        self.add(tree, marker, slots, timeline, scope_tag("schematic"))
        self.at("matching markers should reach")
        wm = marker.copy().move_to(slots[0])
        hm = marker.copy().move_to(slots[1])
        self.play(TransformFromCopy(marker, wm), TransformFromCopy(marker, hm), run_time=1.5)
        self.at("Researchers found")
        found = T("shared insertions: same genome spots", 28, BLUE).move_to([0, -2.55, 0])
        self.play(FadeIn(found, shift=UP * 0.15), run_time=0.8)
        self.at("That pattern groups")
        fit_lab = chip("fits shared ancestry", BLUE, size=30).move_to([3.75, -1.35, 0])
        self.play(FadeIn(fit_lab), Indicate(VGroup(tree.labels[0], tree.labels[1]), color=BLUE), run_time=1.0)
        self.finish()


class S07Relatives(EvidenceScene):
    def construct(self):
        tree = evidence_tree()
        self.add(tree, scope_tag("schematic"))
        bad = Arrow(HIPPO_TIP + DOWN * 0.35, WHALE_TIP + DOWN * 0.35, buff=0.35,
                    color=RED, stroke_width=5)
        self.at("does not mean")
        self.play(GrowArrow(bad), run_time=0.7)
        cross = Cross(bad, stroke_color=RED, stroke_width=7)
        self.play(Create(cross), run_time=0.55)
        self.at("separate tips")
        self.play(FadeOut(bad), FadeOut(cross),
                  tree.labels[0].animate.shift(LEFT * 0.22), tree.labels[1].animate.shift(RIGHT * 0.22), run_time=0.8)
        self.at("share an earlier population")
        glow = Circle(radius=0.3, color=GOLD, stroke_width=7).move_to(FORK)
        self.play(Create(glow), run_time=0.8)
        self.at("each branch continued")
        dots = VGroup(Dot(FORK, radius=0.12, color=GOLD), Dot(FORK, radius=0.12, color=GOLD))
        self.add(dots)
        self.play(MoveAlongPath(dots[0], tree.branches[0]), MoveAlongPath(dots[1], tree.branches[1]), run_time=1.8)
        self.at("Relatives are not")
        cap = caption("Relatives are not automatically ancestors.", color=GOLD)
        self.play(FadeIn(cap), run_time=0.6)
        self.finish()


def bone_set(kind="flipper", center=(3.25, 0.0, 0)):
    """Same green blocks, rearranged into three homologous appendages."""
    c = np.array(center, dtype=float)
    if kind == "flipper":
        pts = [(-1.5, 0), (-0.55, 0), (0.25, 0.35), (0.9, 0.55), (1.45, 0.7)]
    elif kind == "arm":
        pts = [(-1.4, 0.8), (-0.65, 0.25), (0.0, -0.3), (0.65, -0.65), (1.25, -0.85)]
    else:
        pts = [(-1.45, -0.15), (-0.6, 0.1), (0.15, 0.35), (0.95, 0.85), (1.55, 1.35)]
    lengths = (1.15, 0.95, 0.72, 0.62, 0.52)
    g = VGroup()
    for (x, y), length in zip(pts, lengths):
        r = RoundedRectangle(corner_radius=0.08, width=length, height=0.35,
                             stroke_color=GREEN, stroke_width=4,
                             fill_color=GREEN, fill_opacity=0.25).move_to(c + [x, y, 0])
        g.add(r)
    return g


class S08Anatomy(EvidenceScene):
    def construct(self):
        tree = evidence_tree(labels=False).scale(0.55).move_to([-3.8, 0.25, 0])
        self.add(tree, scope_tag("schematic"))
        self.at("Anatomy tests")
        title = T("homologous structures", 34, GREEN, weight=BOLD).move_to([2.5, 2.65, 0])
        self.play(FadeIn(title), run_time=0.7)
        self.at("come from one structure")
        bones = bone_set("flipper")
        self.play(LaggedStart(*[FadeIn(b, scale=0.75) for b in bones], lag_ratio=0.14), run_time=1.2)
        name = T("whale flipper", 30, GREEN).move_to([3.25, -1.75, 0])
        self.at("whale flipper")
        self.play(FadeIn(name), run_time=0.5)
        self.at("human arm")
        arm = bone_set("arm")
        arm_name = T("human arm", 30, GREEN).move_to(name)
        self.play(Transform(bones, arm), swap(name, arm_name), run_time=1.1)
        self.at("bat wing")
        wing = bone_set("wing")
        wing_name = T("bat wing", 30, GREEN).move_to(name)
        self.play(Transform(bones, wing), swap(arm_name, wing_name), run_time=1.1)
        self.at("arranged differently")
        self.play(Indicate(bones, color=GREEN, scale_factor=1.06), run_time=0.8)
        self.finish()


class S09Vestigial(EvidenceScene):
    def construct(self):
        whale = whale_body(GREY, at=[0, 0.25, 0], scale=0.95)
        self.play(FadeIn(whale), run_time=0.8)
        hips = VGroup(
            RoundedRectangle(corner_radius=0.08, width=0.6, height=0.34, stroke_color=GREEN,
                             stroke_width=4, fill_color=GREEN, fill_opacity=0.55).rotate(0.25),
            RoundedRectangle(corner_radius=0.08, width=0.6, height=0.34, stroke_color=GREEN,
                             stroke_width=4, fill_color=GREEN, fill_opacity=0.55).rotate(-0.25),
        ).arrange(RIGHT, buff=0.18).move_to([-0.65, -0.35, 0])
        self.at("small hip bones")
        self.play(FadeIn(hips, scale=0.7), run_time=0.8)
        no_legs = T("no legs attached", 30, GREEN).move_to([0, -2.0, 0])
        self.at("support no legs")
        self.play(FadeIn(no_legs), run_time=0.6)
        self.at("They are vestigial")
        vest = chip("vestigial: reduced", GREEN, size=30).move_to([3.7, -2.15, 0])
        self.play(FadeIn(vest), run_time=0.7)
        self.at("lost all or most")
        old = T("leg support", 28, GREY).move_to([-3.7, -2.2, 0])
        strike = Line(old.get_left(), old.get_right(), color=RED, stroke_width=6)
        strike.layout_ok = True
        self.play(FadeIn(old), Create(strike), run_time=0.8)
        self.at("does not mean useless")
        muscle = ArcBetweenPoints(hips.get_left() + LEFT * 0.5, hips.get_right() + RIGHT * 0.5,
                                  angle=-0.6, color=GREEN, stroke_width=12)
        anchor = T("muscle anchor", 30, GREEN).move_to(old)
        self.play(Create(muscle), FadeOut(strike), swap(old, anchor), run_time=1.0)
        self.at("muscles used in mating")
        self.play(Indicate(VGroup(hips, muscle), color=GREEN, scale_factor=1.08), run_time=0.9)
        self.finish()


class S10Development(EvidenceScene):
    def construct(self):
        whale = whale_body(GREY, at=[0, 0.25, 0], scale=0.82)
        early = embryo_body(at=[-2.35, 0.25, 0], opacity=0.28).scale(0.62)
        later = embryo_body(at=[2.1, 0.25, 0]).scale(0.82)
        arrow = Arrow([-0.25, 0.25, 0], [0.65, 0.25, 0], color=TEAL, stroke_width=5)
        self.add(whale)
        self.at("Development supplies")
        self.play(ReplacementTransform(whale, later), FadeIn(early), GrowArrow(arrow), run_time=1.1)
        buds = VGroup(
            RoundedRectangle(corner_radius=0.09, width=0.72, height=0.38,
                             stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.7),
            RoundedRectangle(corner_radius=0.09, width=0.72, height=0.38,
                             stroke_color=TEAL, stroke_width=4, fill_color=TEAL, fill_opacity=0.7),
        ).arrange(RIGHT, buff=0.4).move_to([1.25, -1.05, 0])
        self.at("begins hindlimb buds")
        self.play(GrowFromCenter(buds), run_time=1.0)
        signal = T("growth signals", 30, TEAL).move_to([2.1, 2.55, 0])
        self.at("signals that keep")
        self.play(FadeIn(signal), buds.animate.scale(1.25), run_time=1.0)
        self.at("switch off early")
        off = T("OFF", 30, RED, weight=BOLD).next_to(signal, RIGHT, buff=0.25)
        self.play(FadeIn(off), run_time=0.7)
        self.at("buds stop")
        self.play(buds.animate.scale(0.08).set_opacity(0), run_time=1.1)
        self.at("not replaying")
        cap = caption("Development is not a replay of ancestors.", color=TEAL)
        self.play(FadeIn(cap), run_time=0.7)
        self.finish()


class S11Converge(EvidenceScene):
    def construct(self):
        tree = evidence_tree(labels=False).scale(0.62).move_to([0.7, 0.15, 0])
        lanes = evidence_lanes(end="✓", y_values=(2.35, 0.85, -0.65, -2.15)).scale(0.72).move_to([0, 0, 0])
        self.at("bring the lanes together")
        self.play(FadeIn(tree), run_time=0.8)
        self.at("Gold fossils")
        self.play(GrowFromEdge(lanes[0], LEFT), run_time=0.8)
        self.at("Blue DNA")
        self.play(GrowFromEdge(lanes[1], LEFT), run_time=0.8)
        self.at("Green anatomy")
        self.play(GrowFromEdge(lanes[2], LEFT), GrowFromEdge(lanes[3], LEFT), run_time=1.1)
        self.at("Different methods")
        self.play(*[Indicate(x[2], color=x[2].get_color(), scale_factor=1.18) for x in lanes], run_time=1.2)
        self.finish()


class S12Limits(EvidenceScene):
    def construct(self):
        lanes = evidence_lanes(end="✓", y_values=(2.5, 0.9, -0.7, -2.3)).scale(0.72)
        self.add(lanes)
        self.at("each test has limits")
        head = T("agreement is not certainty", 34, TEXT, weight=BOLD).move_to([0, 3.25, 0])
        self.play(FadeIn(head), run_time=0.7)
        self.at("Fossil sequences")
        n1 = T("not direct parents", 28, GOLD).move_to([1.6, 1.25, 0])
        self.play(FadeIn(n1), run_time=0.7)
        self.at("Similarity matters")
        n2 = T("compare matching regions", 28, BLUE).move_to([1.6, 0.12, 0])
        self.play(FadeIn(n2), run_time=0.7)
        self.at("useful structure")
        n3 = T("function may remain", 28, GREEN).move_to([1.6, -1.0, 0])
        self.play(FadeIn(n3), run_time=0.7)
        self.play(*[Indicate(x, color=x.get_color(), scale_factor=1.05) for x in (n1, n2, n3)], run_time=0.9)
        self.finish()


class S13Theory(EvidenceScene):
    def construct(self):
        tree = evidence_tree(labels=False).scale(0.58).move_to([0.8, 0.0, 0]).set_opacity(0.45)
        qs = evidence_lanes(end="?", y_values=(2.35, 0.85, -0.65, -2.15)).scale(0.72)
        self.add(tree, qs)
        self.at("tested explanation")
        head = T("theory = tested explanation", 34, GOLD, weight=BOLD).move_to([0, 3.25, 0])
        self.play(FadeIn(head), run_time=0.8)
        self.at("predicts related patterns")
        self.play(*[Indicate(x[2], color=x[2].get_color(), scale_factor=1.2) for x in qs], run_time=1.0)
        self.at("before each evidence lane")
        self.play(*[FadeOut(x[2]) for x in qs], run_time=0.55)
        checks = VGroup(*[T("✓", 34, col, weight=BOLD).next_to(qs[i][0].get_end(), RIGHT, buff=0.16)
                          for i, col in enumerate((GOLD, BLUE, GREEN, TEAL))])
        self.at("Confidence grows")
        self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in checks], lag_ratio=0.22), run_time=1.5)
        self.at("across methods")
        outline = RoundedRectangle(corner_radius=0.25, width=12.2, height=5.8,
                                   stroke_color=TEXT, stroke_width=3).move_to([0, 0, 0])
        outline.layout_ok = True
        self.play(Create(outline), run_time=0.8)
        self.finish()


class S14Rule(EvidenceScene):
    def construct(self):
        tree = evidence_tree(labels=False).scale(0.58).move_to([0.8, 0.0, 0]).set_opacity(0.55)
        lanes = evidence_lanes(end="✓", y_values=(2.35, 0.85, -0.65, -2.15)).scale(0.72)
        self.add(tree, lanes)
        self.at("could have pointed")
        self.play(*[x[0].animate.rotate(a, about_point=x[0].get_start())
                    for x, a in zip(lanes, (0.08, -0.08, 0.06, -0.06))], run_time=1.0)
        self.at("patterns agree")
        self.play(*[x[0].animate.rotate(-a, about_point=x[0].get_start())
                    for x, a in zip(lanes, (0.08, -0.08, 0.06, -0.06))], run_time=1.0)
        self.at("Independent evidence")
        outline = RoundedRectangle(corner_radius=0.28, width=13.6, height=5.3,
                                   stroke_color=TEXT, stroke_width=4).move_to([0, 0.1, 0])
        outline.layout_ok = True
        self.play(Create(outline), run_time=1.0)
        self.at("strengthens an explanation")
        cap = caption("Independent agreement strengthens common descent.", color=GOLD)
        self.play(FadeIn(cap), *[Indicate(x[2], color=x[2].get_color(), scale_factor=1.12) for x in lanes], run_time=1.2)
        pulse(outline, base=4, amp=1.2, speed=2.0)
        self.finish()


class S15End(EndCard):
    LINE = "Independent evidence that agrees strengthens an explanation of common descent."
