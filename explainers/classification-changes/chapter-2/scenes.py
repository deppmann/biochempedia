"""When Evidence Redraws a Branch — classification changes, chapter 2.

COLOR MAP (kept throughout this chapter)
  TEAL  = Archaea
  BAC   = Bacteria
  GOLD  = Eukarya and its organisms
  TEXT  = evidence and evidence cards
  GREY  = provisional structure / secondary annotation

The tree and the Eukarya close-up are rebuilt only through the builders below so their
landmarks never drift between scenes.  Every relationship shown is explicitly schematic.
"""
from bp_parts import *  # noqa: F401,F403

BAC = "#7D8CFF"


def branch_glow(lines, width=110):
    """Broad, faint copies make the active branch fill the frame and breathe continuously."""
    glow = VGroup(*[ln.copy().set_stroke(width=width, opacity=0.23) for ln in lines])
    for i, ln in enumerate(glow):
        pulse(ln, base=width, amp=10, speed=0.72 + i * 0.07)
    bob(glow, amp=0.14, speed=1.2)
    return glow


def evidence_card(text="evidence", width=None):
    """A white evidence card; this is a claim card, not a molecule."""
    label = fit_text(text, max_w=(width or 3.0) - 0.35, size=28, color=TEXT, max_lines=2)
    w = width or max(2.2, label.width + 0.55)
    box = RoundedRectangle(corner_radius=0.16, width=w, height=max(0.78, label.height + 0.35),
                           stroke_color=TEXT, stroke_width=3, fill_color=BG, fill_opacity=0.96)
    return VGroup(box, label.move_to(box))


def organism_icon(kind, center, color=GOLD, scale=1.0):
    """Simple labelled cartoons: no anatomical or molecular claims."""
    c = np.array(center, dtype=float)
    if kind == "plant":
        stem = Line(c + DOWN * 0.45, c + UP * 0.45, color=color, stroke_width=7)
        leaves = VGroup(Ellipse(0.55, 0.28, color=color, fill_color=color, fill_opacity=0.22).rotate(0.45).move_to(c + [-0.26, 0.12, 0]),
                        Ellipse(0.55, 0.28, color=color, fill_color=color, fill_opacity=0.22).rotate(-0.45).move_to(c + [0.26, 0.30, 0]))
        art = VGroup(stem, leaves)
    elif kind == "mushroom":
        cap = ArcBetweenPoints(c + [-0.62, 0.18, 0], c + [0.62, 0.18, 0], angle=-PI,
                               color=color, stroke_width=7)
        stalk = RoundedRectangle(corner_radius=0.12, width=0.42, height=0.75, color=color,
                                 stroke_width=5, fill_color=color, fill_opacity=0.14).move_to(c + DOWN * 0.18)
        art = VGroup(stalk, cap)
    elif kind == "animal":
        body = Ellipse(1.15, 0.7, color=color, stroke_width=6, fill_color=color, fill_opacity=0.14).move_to(c)
        head = Circle(0.28, color=color, stroke_width=5, fill_color=color, fill_opacity=0.14).move_to(c + [0.62, 0.18, 0])
        legs = VGroup(Line(c + [-0.32, -0.28, 0], c + [-0.38, -0.65, 0], color=color, stroke_width=5),
                      Line(c + [0.28, -0.28, 0], c + [0.34, -0.65, 0], color=color, stroke_width=5))
        art = VGroup(body, head, legs)
    elif kind == "whale":
        body = Ellipse(1.75, 0.72, color=color, stroke_width=6, fill_color=color, fill_opacity=0.14).move_to(c)
        tail = VGroup(Line(c + [-0.82, 0, 0], c + [-1.18, 0.38, 0], color=color, stroke_width=6),
                      Line(c + [-0.82, 0, 0], c + [-1.18, -0.38, 0], color=color, stroke_width=6))
        art = VGroup(body, tail)
    elif kind == "hippo":
        body = RoundedRectangle(corner_radius=0.38, width=1.55, height=0.82, color=color,
                                stroke_width=6, fill_color=color, fill_opacity=0.14).move_to(c)
        art = VGroup(body, Dot(c + [0.48, 0.10, 0], radius=0.05, color=color))
    else:
        art = Circle(0.5, color=color, stroke_width=6, fill_color=color, fill_opacity=0.14).move_to(c)
    art.scale(scale)
    art.kind = kind
    return art


def full_tree(with_labels=True):
    """The shared full tree; root and every joint have fixed coordinates."""
    root = np.array([0.0, -2.35, 0.0])
    j_a = np.array([-1.8, -0.65, 0.0])
    j_e = np.array([2.0, -0.35, 0.0])
    lines = VGroup(
        Line(root, [-4.65, 1.72, 0], color=BAC, stroke_width=9),
        Line(root, j_a, color=TEAL, stroke_width=9),
        Line(j_a, [-0.65, 1.72, 0], color=TEAL, stroke_width=9),
        Line(root, j_e, color=GOLD, stroke_width=9),
        Line(j_e, [3.15, 1.72, 0], color=GOLD, stroke_width=9),
        Line(j_e, [5.2, 1.72, 0], color=GOLD, stroke_width=9),
    )
    joints = VGroup(Dot(root, radius=0.09, color=GREY), Dot(j_a, radius=0.10, color=TEAL), Dot(j_e, radius=0.11, color=GOLD))
    glow = branch_glow(lines)
    g = VGroup(glow, lines, joints)
    g.glow, g.lines, g.joints, g.euk_joint = glow, lines, joints, joints[2]
    if with_labels:
        labels = VGroup(T("Bacteria", 30, BAC).move_to([-4.65, 2.2, 0]),
                        T("Archaea", 30, TEAL).move_to([-0.65, 2.2, 0]),
                        T("Eukarya", 30, GOLD).move_to([4.15, 2.55, 0]))
        g.add(labels)
        g.labels = labels
    return g


def eukarya_world(grouping="plant", icons=True):
    """The fixed gold close-up used for appearance, proteins, and repeated testing."""
    root = np.array([0.0, -2.15, 0.0])
    plant, fungus, animal = np.array([-4.3, 1.5, 0]), np.array([0.0, 1.5, 0]), np.array([4.3, 1.5, 0])
    if grouping == "plant":
        joint = np.array([-2.15, -0.15, 0])
        lines = VGroup(Line(root, joint, color=GOLD, stroke_width=9),
                       Line(joint, plant, color=GOLD, stroke_width=9),
                       DashedLine(joint, fungus, color=GOLD, stroke_width=7, dash_length=0.18),
                       Line(root, animal, color=GOLD, stroke_width=9))
    else:
        joint = np.array([2.15, -0.15, 0])
        lines = VGroup(Line(root, plant, color=GOLD, stroke_width=9),
                       Line(root, joint, color=GOLD, stroke_width=9),
                       Line(joint, fungus, color=GOLD, stroke_width=9),
                       Line(joint, animal, color=GOLD, stroke_width=9))
    dots = VGroup(Dot(root, radius=0.10, color=GREY), Dot(joint, radius=0.13, color=GOLD))
    glow = branch_glow(lines)
    g = VGroup(glow, lines, dots)
    g.glow, g.lines, g.joint = glow, lines, dots[1]
    if icons:
        arts = VGroup(organism_icon("plant", plant + UP * 0.15), organism_icon("mushroom", fungus + UP * 0.15),
                      organism_icon("animal", animal + UP * 0.15))
        labels = VGroup(T("plant", 28, GOLD).move_to(plant + UP * 1.35),
                        T("fungus", 28, GOLD).move_to(fungus + UP * 1.35),
                        T("animal", 28, GOLD).move_to(animal + UP * 1.35))
        g.add(arts, labels)
        g.arts, g.labels = arts, labels
    return g


def branch_question_backdrop(card_x=-4.6):
    tree = eukarya_world("animal", icons=False).scale(0.72).shift(LEFT * 1.45 + UP * 0.15)
    card = evidence_card("supports this joint", 2.7).move_to([card_x, 1.55, 0])
    arrow = Arrow(card.get_right(), tree.joint.get_center() + LEFT * 0.25, buff=0.15, color=TEXT,
                  stroke_width=5, tip_length=0.22)
    return VGroup(tree, card, arrow)


def protein_rows():
    rows = VGroup()
    for y, name in ((1.0, "plant"), (0.1, "fungus"), (-0.8, "animal")):
        label = T(name, 28, GOLD).move_to([-4.85, y, 0])
        blocks = VGroup(*[RoundedRectangle(corner_radius=0.07, width=0.62, height=0.42,
                                          stroke_color=TEXT, stroke_width=3, fill_color=TEXT,
                                          fill_opacity=0.16).move_to([-3.5 + i * 0.78, y, 0]) for i in range(8)])
        if name == "plant":
            blocks[4].set_opacity(0.18)
        else:
            blocks[4].set_stroke(GOLD, width=5).set_fill(GOLD, opacity=0.35)
        rows.add(VGroup(label, blocks))
    return rows


class S00Link(SpokenScene):
    def construct(self):
        tree = full_tree()
        for ln in tree.lines:
            pulse(ln, base=9, amp=1.0, speed=1.5)
        self.play(FadeIn(tree.glow), Create(tree.lines), FadeIn(tree.joints), FadeIn(tree.labels), run_time=1.0)
        self.add(scope_tag("schematic"))
        self.at("How do we decide")
        self.play(tree.animate.scale(1.12).shift(LEFT * 0.55), run_time=1.0)
        self.at("current tree as a claim")
        claim = evidence_card("current claim", 2.45).move_to([2.8, -1.35, 0])
        lead = Line(claim.get_left(), tree.euk_joint.get_center(), color=TEXT, stroke_width=3)
        self.play(FadeIn(claim, shift=LEFT * 0.2), Create(lead), run_time=0.8)
        self.at("each new comparison")
        ev = evidence_card("new comparison", 2.75).move_to([4.65, 0.2, 0])
        self.play(FadeIn(ev, shift=LEFT * 0.3), ev.animate.shift(LEFT * 0.25), run_time=1.1)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Classification changes"
    TITLE = "When Evidence Redraws a Branch"


class S02Appearance(SpokenScene):
    def construct(self):
        world = eukarya_world("plant")
        for art in world.arts:
            bob(art, amp=0.045, speed=1.3)
        self.play(FadeIn(world.glow), Create(world.lines), FadeIn(world.joint), run_time=0.8)
        self.at("grow in place")
        self.play(FadeIn(world.arts[0]), FadeIn(world.arts[1]), FadeIn(world.labels[0]), FadeIn(world.labels[1]), run_time=0.8)
        self.at("mushroom icon begins")
        self.play(FadeIn(world.arts[2]), FadeIn(world.labels[2]), run_time=0.6)
        self.at("placement is a hypothesis")
        hyp = evidence_card("hypothesis", 2.25).move_to([-2.15, -0.85, 0])
        appearance = evidence_card("appearance", 2.25).move_to([-2.15, 2.75, 0])
        self.play(FadeIn(appearance, shift=DOWN * 0.15), FadeIn(hyp), run_time=0.8)
        self.at("branch must survive")
        tests = VGroup(*[evidence_card(x, 1.55) for x in ("test 1", "test 2")]).arrange(RIGHT, buff=0.3).move_to([2.3, -2.75, 0])
        self.play(FadeOut(hyp), FadeIn(tests, shift=UP * 0.2), run_time=0.9)
        self.add(scope_tag("schematic"))
        self.finish()


class S03Proteins(SpokenScene):
    def construct(self):
        old = eukarya_world("plant")
        self.add(old, scope_tag("schematic"))
        self.at("Protein comparisons")
        card = evidence_card("protein comparisons", 3.25).move_to([-4.55, -2.85, 0])
        self.play(FadeIn(card, shift=DOWN * 0.2), run_time=0.7)
        self.at("Several protein trees")
        rows = protein_rows()
        bob(rows, amp=0.055, speed=0.75)
        scan = Rectangle(width=0.72, height=2.75, stroke_width=0, fill_color=TEXT, fill_opacity=0.16).move_to([-3.65, 0.1, 0])
        scan._sweep_t = 0.0

        def sweep(mob, dt):
            mob._sweep_t += dt
            mob.set_x(-3.65 + 5.35 * (0.5 + 0.5 * np.sin(1.65 * mob._sweep_t)))

        scan.add_updater(sweep)
        rows.add(scan)
        self.play(FadeOut(old.arts), FadeOut(old.labels), old.animate.scale(0.58).shift(RIGHT * 3.5 + DOWN * 0.45),
                  FadeIn(rows, shift=RIGHT * 0.2), run_time=1.0)
        self.at("Shared added or missing")
        match = VGroup(rows[1][1][4], rows[2][1][4])
        self.play(Indicate(match, color=TEXT, scale_factor=1.12), run_time=1.0)
        self.at("mushroom branch slides")
        new = eukarya_world("animal", icons=False).scale(0.58).shift(RIGHT * 3.5 + DOWN * 0.45)
        self.play(FadeOut(rows), ReplacementTransform(old, new), run_time=1.2)
        ancestor = evidence_card("shared ancestor", 2.75).move_to([2.35, -1.75, 0])
        self.play(FadeIn(ancestor), run_time=0.5)
        self.at("does not mean")
        note = caption("A shared ancestor is not a modern mushroom.", color=TEXT)
        self.play(FadeOut(card), FadeIn(note), run_time=0.7)
        self.finish()


class S04Repeat(SpokenScene):
    def construct(self):
        tree = eukarya_world("animal", icons=False)
        pulse(tree.lines[1], base=9, amp=1.2, speed=1.4)
        self.add(tree, scope_tag("schematic"))
        self.at("A result can be a clue")
        cards = VGroup(evidence_card("comparison A", 2.35), evidence_card("comparison B", 2.35),
                       evidence_card("comparison C", 2.35)).arrange(DOWN, buff=0.26).move_to([-4.65, 0.45, 0])
        self.play(FadeIn(cards[0], shift=RIGHT * 0.25), run_time=0.7)
        self.at("different comparisons")
        self.play(FadeIn(cards[1], shift=RIGHT * 0.25), cards[0].animate.shift(RIGHT * 0.35),
                  cards[1].animate.shift(RIGHT * 0.35), run_time=1.0)
        self.at("sampling is broad")
        broad = evidence_card("broad samples", 2.35).move_to([-3.7, -1.9, 0])
        self.play(FadeIn(broad, shift=UP * 0.2), run_time=0.7)
        self.at("Conflicting results")
        question = evidence_card("comparison ?", 2.35).move_to([-4.65, -0.55, 0])
        self.play(ReplacementTransform(cards[2], question), run_time=0.9)
        self.at("methods")
        checks = VGroup(*[chip(x, TEXT, 28) for x in ("methods", "markers", "samples")]).arrange(RIGHT, buff=0.25).move_to([1.7, -2.85, 0])
        self.play(FadeIn(checks[0]), run_time=0.4)
        self.at("markers")
        self.play(FadeIn(checks[1]), run_time=0.4)
        self.at("organisms")
        self.play(FadeIn(checks[2]), run_time=0.4)
        self.at("open to testing")
        self.play(Rotate(tree.joint, angle=TAU, run_time=1.0), run_time=1.0)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        back = branch_question_backdrop(-5.2)
        self.add(back[0], scope_tag("schematic"))
        card, arrow = back[1], back[2]
        self.at("new evidence card")
        self.play(FadeIn(card), GrowArrow(arrow), card.animate.shift(RIGHT * 0.7), run_time=3.4, rate_func=linear)
        self.at("Should scientists")
        q = question_card("What should scientists do?", ["move", "keep", "erase all"], chips_at=[4.75, 0.55, 0])
        self.play(FadeIn(q.question), run_time=0.5)
        self.at("move that branch")
        self.play(FadeIn(q.chips[0]), run_time=0.35)
        self.at("keep it")
        self.play(FadeIn(q.chips[1]), run_time=0.35)
        self.at("erase the whole tree")
        self.play(FadeIn(q.chips[2]), run_time=0.35)
        self.at("Choose before")
        self.play(card.animate.shift(RIGHT * 0.65), run_time=1.3, rate_func=linear)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "What should scientists do?"
    OPTIONS = ["move", "keep", "erase all"]
    CHIPS_AT = [4.75, 0.55, 0]
    SECONDS = 4.5

    def backdrop(self):
        tag = T("schematic", 24, GREY).move_to([5.75, 3.35, 0])
        return VGroup(branch_question_backdrop(-3.85), tag)


class S07Reveal(SpokenScene):
    def construct(self):
        tree = eukarya_world("animal", icons=False)
        card = evidence_card("supports this joint", 2.7).move_to([-3.85, 1.55, 0])
        self.add(tree, card, scope_tag("schematic"))
        self.at("Keep it")
        keep = chip("KEEP", GOLD, 38).move_to([4.65, 2.4, 0])
        self.play(FadeIn(keep, scale=0.85), card.animate.move_to(tree.joint.get_center() + LEFT * 1.6), run_time=1.0)
        self.at("does not require movement")
        self.play(Indicate(tree.joint, color=TEXT, scale_factor=1.45), run_time=0.9)
        self.at("strengthen the present")
        self.play(tree.lines[1].animate.set_stroke(width=13), tree.lines[2].animate.set_stroke(width=13),
                  tree.lines[3].animate.set_stroke(width=13), run_time=1.2)
        self.at("Revision belongs")
        rule = caption("Revise where evidence changes the picture.", color=TEXT)
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.8)
        self.at("not rebuild every branch")
        full = full_tree()
        for ln in full.lines:
            pulse(ln, base=9, amp=0.8, speed=1.25)
        self.play(FadeOut(VGroup(tree, card, keep, rule)), FadeIn(full), run_time=1.2)
        self.finish()


def elephant(kind, center):
    c = np.array(center, dtype=float)
    col = GOLD
    body = Ellipse(2.0 if kind == "savanna" else 1.7, 1.15, color=col, stroke_width=6,
                   fill_color=col, fill_opacity=0.14).move_to(c)
    head = Circle(0.48, color=col, stroke_width=5, fill_color=col, fill_opacity=0.14).move_to(c + [0.85, 0.18, 0])
    trunk = ArcBetweenPoints(c + [1.13, 0.1, 0], c + [1.15, -0.72, 0], angle=-0.5, color=col, stroke_width=6)
    return VGroup(body, head, trunk)


class S08Elephants(SpokenScene):
    def construct(self):
        root = Dot([0, -1.55, 0], radius=0.12, color=GOLD)
        branches = VGroup(Line(root, [-3.2, 0.65, 0], color=GOLD, stroke_width=9),
                          Line(root, [3.2, 0.65, 0], color=GOLD, stroke_width=9))
        left, right = elephant("forest", [-3.2, 1.05, 0]), elephant("savanna", [3.2, 1.05, 0])
        bob(left, amp=0.04, speed=1.2); bob(right, amp=0.04, speed=1.4)
        glow = branch_glow(branches, width=88)
        self.play(FadeIn(root), FadeIn(glow), Create(branches), FadeIn(left), FadeIn(right), run_time=1.0)
        self.at("Nuclear DNA")
        title = evidence_card("nuclear DNA", 2.6).move_to([0, 2.75, 0])
        self.play(FadeIn(title), run_time=0.6)
        self.at("separate species")
        labels = VGroup(T("forest", 30, GOLD).move_to([-3.2, 2.25, 0]), T("savanna", 30, GOLD).move_to([3.2, 2.25, 0]))
        self.play(FadeIn(labels), branches.animate.set_stroke(width=12), run_time=0.8)
        self.at("sampled very few")
        samples = VGroup(*[Dot(radius=0.14, color=TEXT) for _ in range(6)]).arrange(RIGHT, buff=0.24).move_to([-1.7, -2.85, 0])
        small = chip("small sample", TEXT, 28).move_to([2.0, -2.85, 0])
        self.play(FadeIn(samples), FadeIn(small), run_time=0.7)
        self.at("Broad stretches of DNA")
        blocks = VGroup(*[Rectangle(width=0.42, height=0.34, stroke_color=TEXT, stroke_width=2,
                                    fill_color=TEXT, fill_opacity=0.25) for _ in range(18)]).arrange(RIGHT, buff=0.09).move_to([0, -1.95, 0])
        self.play(LaggedStart(*[FadeIn(b) for b in blocks], lag_ratio=0.045), run_time=1.3)
        self.at("limit visible")
        self.play(Indicate(small, color=TEXT, scale_factor=1.08), run_time=0.8)
        self.add(scope_tag("schematic"))
        self.finish()


class S08More(SpokenScene):
    def construct(self):
        joint = Dot([0, -1.4, 0], radius=0.13, color=GOLD)
        lines = VGroup(Line(joint, [-3.0, 0.5, 0], color=GOLD, stroke_width=9), Line(joint, [3.0, 0.5, 0], color=GOLD, stroke_width=9))
        whale, hippo = organism_icon("whale", [-3.0, 1.0, 0]), organism_icon("hippo", [3.0, 1.0, 0])
        bob(whale, amp=0.04); bob(hippo, amp=0.04, seed=2)
        glow = branch_glow(lines, width=88)
        self.play(FadeIn(joint), FadeIn(glow), Create(lines), FadeIn(whale), FadeIn(hippo), run_time=1.0)
        dna = evidence_card("DNA comparisons", 2.9).move_to([0, 2.65, 0])
        self.play(FadeIn(dna), run_time=0.6)
        self.at("with hippos")
        labs = VGroup(T("whale", 30, GOLD).move_to([-3, 1.85, 0]), T("hippo", 30, GOLD).move_to([3, 1.85, 0]))
        self.play(FadeIn(labs), Indicate(joint, color=TEXT), run_time=0.8)
        self.at("Gene sequences")
        prot_root = Dot([0, -1.65, 0], radius=0.12, color=GOLD)
        tips = [-4.6, -2.6, -0.8, 1.0, 2.8, 4.8]
        prot_lines = VGroup(*[Line(prot_root, [x, 1.05 + 0.25 * (i % 2), 0], color=GOLD, stroke_width=7) for i, x in enumerate(tips)])
        prot_glow = branch_glow(prot_lines, width=68)
        gene = evidence_card("gene sequences", 2.8).move_to([0, 2.65, 0])
        self.play(FadeOut(VGroup(joint, lines, whale, hippo, labs)), ReplacementTransform(dna, gene),
                  FadeIn(prot_root), FadeIn(prot_glow), LaggedStart(*[Create(x) for x in prot_lines], lag_ratio=0.1), run_time=1.5)
        prot = T("many protist branches", 32, GOLD).move_to([0, 1.95, 0])
        self.play(FadeOut(gene), FadeIn(prot), run_time=0.5)
        self.at("differ in scale")
        scale_tag = chip("different scales", TEXT, 28).move_to([-4.8, -2.45, 0])
        self.play(FadeIn(scale_tag), run_time=0.6)
        self.at("which tree fits")
        fit_tag = chip("tree fits evidence", TEXT, 28).move_to([0, -2.45, 0])
        self.play(FadeIn(fit_tag), run_time=0.6)
        self.at("own evidence")
        limit = chip("evidence + limits", TEXT, 28).move_to([4.55, -2.45, 0])
        self.play(FadeIn(limit), run_time=0.7)
        self.add(scope_tag("schematic"))
        self.finish()


class S09Model(SpokenScene):
    def construct(self):
        old = eukarya_world("plant")
        for a in old.arts:
            bob(a, amp=0.035, speed=1.2)
        self.play(FadeIn(old), run_time=0.8)
        self.at("changes the scientific model")
        model = chip("scientific model", TEXT, 30).move_to([0, -2.9, 0])
        self.play(FadeIn(model), run_time=0.6)
        self.at("does not make organisms")
        fixed_icons = old.arts.copy()
        new = eukarya_world("animal")
        self.play(FadeOut(old.lines), FadeOut(old.joint), FadeIn(new.lines), FadeIn(new.joint), run_time=1.2)
        self.at("earlier scientists careless")
        older = evidence_card("evidence available then", 3.55).move_to([-3.1, -2.75, 0])
        self.play(FadeOut(model), FadeIn(older, shift=UP * 0.15), run_time=0.7)
        self.at("evidence available")
        self.play(Indicate(older, color=TEXT, scale_factor=1.05), run_time=0.7)
        self.at("Better tools")
        newer = evidence_card("better tools • new patterns", 3.75).move_to([3.1, -2.75, 0])
        self.play(FadeIn(newer, shift=UP * 0.15), run_time=0.8)
        self.at("shape")
        self.play(Indicate(new.lines, color=TEXT, scale_factor=1.03), run_time=0.7)
        self.add(scope_tag("schematic"))
        self.finish()


class S10Close(SpokenScene):
    def construct(self):
        tree = full_tree()
        for ln in tree.lines:
            pulse(ln, base=9, amp=0.9, speed=1.25)
        self.play(FadeIn(tree), run_time=0.8)
        self.add(scope_tag("schematic"))
        self.at("What relationship")
        old = evidence_card("old claim?", 2.3).move_to([-4.7, -2.7, 0])
        self.play(FadeIn(old, shift=UP * 0.15), run_time=0.7)
        self.at("What new pattern")
        new = evidence_card("new pattern?", 2.55).move_to([0, -2.7, 0])
        self.play(FadeIn(new, shift=UP * 0.15), run_time=0.7)
        self.at("What important limits")
        limits = evidence_card("limits?", 2.2).move_to([4.7, -2.7, 0])
        self.play(FadeIn(limits, shift=UP * 0.15), run_time=0.7)
        self.at("Those questions turn")
        self.play(old.animate.move_to([-2.1, 0.25, 0]), new.animate.move_to([2.0, 0.6, 0]),
                  limits.animate.move_to([3.75, -0.95, 0]), run_time=1.4)
        self.at("scientific explanation")
        rule = caption("Explain the changed relationship, evidence, and limits.", color=TEXT)
        self.play(FadeIn(rule, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S11End(EndCard):
    LINE = "Classification changes when new evidence\nchanges the best-supported picture of ancestry."
