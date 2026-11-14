"""Classification changes: The Molecule Behind the Tree.

COLOR MAP
  BAC = typical Bacteria (blue)
  TEAL = methane makers / Archaea
  GOLD = Eukarya
  TEXT = evidence and supported claims
  GREY = unresolved or de-emphasised structure

All carried cells and trees are rebuilt by the builders below so their scale and
landmarks stay fixed from scene to scene.  RNA is represented only as labelled
rectangular records; no molecular structure is drawn.
"""
from bp_parts import *  # noqa: F401,F403

BAC = "#6F86FF"
EUK = GOLD


class LivingScene(SpokenScene):
    """Spoken scene on the film's one gently scanned diagram board."""

    def setup(self):
        super().setup()
        board = RoundedRectangle(
            corner_radius=0.30, width=12.55, height=6.55,
            stroke_color=GREY, stroke_width=2,
            fill_color=GREY, fill_opacity=0.18,
        ).set_z_index(-50)
        scan = Rectangle(width=0.82, height=6.10, stroke_width=0,
                         fill_color=TEAL, fill_opacity=0.30).set_z_index(-49)
        scan._x = -5.85
        scan.move_to([scan._x, 0, 0])

        def sweep(mob, dt):
            mob._x += 1.60 * dt
            if mob._x > 5.85:
                mob._x = -5.85
            mob.move_to([mob._x, 0, 0])

        scan.add_updater(sweep)
        board.layout_ok = True  # background diagram board intentionally sits behind all labels
        scan.layout_ok = True   # faint focus sweep intentionally passes behind the diagram
        self.add(board, scan)


def cell_icon(color, label=None, nucleus=False, at=ORIGIN, scale=1.0):
    """The film's large schematic cell; intentionally not a molecular drawing."""
    body = RoundedRectangle(
        corner_radius=0.52, width=2.25, height=1.35,
        stroke_color=color, stroke_width=5,
        fill_color=color, fill_opacity=0.15,
    )
    inner = VGroup(
        Dot([-0.50, 0.18, 0], radius=0.10, color=TEXT),
        Dot([0.10, -0.25, 0], radius=0.10, color=TEXT),
        Dot([0.54, 0.28, 0], radius=0.10, color=TEXT),
    )
    if nucleus:
        inner.add(Circle(radius=0.30, color=EUK, stroke_width=4).move_to([-0.22, 0.08, 0]))
    g = VGroup(body, inner)
    if label:
        g.add(T(label, 32, color, weight=BOLD).next_to(body, DOWN, buff=0.16))
    g.scale(scale).move_to(at)
    return g


def tree_world(labels=False, model_tag=False, at=ORIGIN, scale=1.0):
    """The carried three-tip tree. Every branch landmark is defined here."""
    root = np.array([0.0, -2.15, 0.0])
    joint = np.array([0.0, -0.72, 0.0])
    tips = [np.array([-3.55, 1.72, 0]), np.array([0.0, 2.22, 0]), np.array([3.55, 1.72, 0])]
    lines = VGroup(
        Line(root, joint, color=GREY, stroke_width=9),
        Line(joint, tips[0], color=BAC, stroke_width=9),
        Line(joint, tips[1], color=TEAL, stroke_width=9),
        Line(joint, tips[2], color=EUK, stroke_width=9),
    )
    nodes = VGroup(Dot(root, radius=0.13, color=TEXT), Dot(joint, radius=0.16, color=TEXT))
    icons = VGroup(
        cell_icon(BAC, at=tips[0] + UP * 0.42, scale=0.53),
        cell_icon(TEAL, at=tips[1] + UP * 0.42, scale=0.53),
        cell_icon(EUK, nucleus=True, at=tips[2] + UP * 0.42, scale=0.53),
    )
    g = VGroup(lines, nodes, icons)
    if labels:
        labs = VGroup(
            T("Bacteria", 30, BAC, weight=BOLD).next_to(icons[0], UP, buff=0.06),
            T("Archaea", 30, TEAL, weight=BOLD).next_to(icons[1], UP, buff=0.06),
            T("Eukarya", 30, EUK, weight=BOLD).next_to(icons[2], UP, buff=0.06),
        )
        g.add(labs)
    if model_tag:
        g.add(T("best-supported model", 34, TEXT).move_to([0, -2.62, 0]))
    g.scale(scale).move_to(at)
    return g


def unresolved_tree(at=(3.75, 0.35, 0), scale=0.72):
    root = np.array([0, -2.0, 0])
    joint = np.array([0, -0.45, 0])
    tips = [np.array([-1.55, 1.55, 0]), np.array([1.55, 1.55, 0])]
    g = VGroup(
        Line(root, joint, color=GREY, stroke_width=8),
        Line(joint, tips[0], color=GREY, stroke_width=8),
        Line(joint, tips[1], color=GREY, stroke_width=8),
        Dot(joint, radius=0.15, color=TEXT),
    )
    return g.scale(scale).move_to(at)


def rna_strip(color=TEXT, at=ORIGIN, width=2.8):
    box = RoundedRectangle(corner_radius=0.12, width=width, height=0.52,
                           stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.18).move_to(at)
    return VGroup(box, T("ribosomal RNA", 24, color).move_to(box))


def tile_row(pattern, color=TEXT, at=ORIGIN, scale=1.0):
    tiles = VGroup()
    for i, value in enumerate(pattern):
        col = color if value else GREY
        r = RoundedRectangle(corner_radius=0.08, width=0.66, height=0.56,
                             stroke_color=col, stroke_width=3,
                             fill_color=col, fill_opacity=0.22)
        t = M(chr(65 + i), 24, col)
        tiles.add(VGroup(r, t.move_to(r)))
    tiles.arrange(RIGHT, buff=0.12).scale(scale).move_to(at)
    return tiles


def pair_diagram(matches, color_a=TEAL, color_b=TEAL, at=ORIGIN, width=4.4):
    """Two six-tile catalogues; matches are explicit data in this schematic."""
    top = tile_row([1] * 6, color_a, at=UP * 0.58)
    bottom = tile_row([1] * 6, color_b, at=DOWN * 0.58)
    links = VGroup()
    for i in range(matches):
        links.add(Line(top[i].get_bottom(), bottom[i].get_top(), color=TEXT, stroke_width=4))
    g = VGroup(links, top, bottom)
    fit(g, max_w=width)
    g.move_to(at)
    return g


def predict_backdrop():
    many = pair_diagram(5, TEXT, TEXT, at=[-3.35, 0.60, 0], width=4.7)
    few = pair_diagram(2, TEXT, TEXT, at=[3.35, 0.60, 0], width=4.7)
    q1 = T("?", 48, GOLD, weight=BOLD).next_to(many, UP, buff=0.18)
    q2 = T("?", 48, GOLD, weight=BOLD).next_to(few, UP, buff=0.18)
    bob(many, amp=0.07, speed=1.4)
    bob(few, amp=0.07, speed=1.2, seed=2)
    return VGroup(many, few, q1, q2)


class S00Hook(LivingScene):
    def construct(self):
        ring = Circle(radius=2.55, color=GREY, stroke_width=7, fill_color=GREY, fill_opacity=0.04)
        a = cell_icon(TEAL, at=[-1.18, 0.15, 0], scale=0.92)
        b = cell_icon(BAC, at=[1.18, 0.15, 0], scale=0.92)
        bob(a, amp=0.10, speed=1.5)
        bob(b, amp=0.10, speed=1.7, seed=2)
        self.at("These methane making microbes")
        self.play(Create(ring), FadeIn(a, scale=0.8), run_time=1.1)
        self.at("look like typical bacteria")
        self.play(FadeIn(b, scale=0.8), Rotate(a, angle=0.10), Rotate(b, angle=-0.10), run_time=1.2)
        q = fit_text("Why a different branch?", max_w=6.2, size=40, color=GOLD, weight=BOLD).move_to([0, -3.0, 0])
        self.at("Why would a molecule")
        self.play(FadeIn(q, shift=UP * 0.2), ring.animate.set_stroke(color=TEXT), run_time=1.0)
        tiny = T("tiny cells • no nuclei", 30, TEXT).move_to([0, 3.05, 0])
        self.at("Under the microscope")
        self.play(FadeIn(tiny), Rotate(a, angle=-0.18), Rotate(b, angle=0.18), run_time=1.3)
        tree = unresolved_tree(at=[0, 0.15, 0], scale=1.15)
        self.at("Shape gives us evidence")
        self.play(FadeOut(q), FadeOut(tiny), ReplacementTransform(ring, tree),
                  a.animate.scale(0.65).move_to([-2.35, 1.95, 0]),
                  b.animate.scale(0.65).move_to([2.35, 1.95, 0]), run_time=1.7)
        tag = scope_tag("schematic")
        hidden = caption("Shape may hide ancestry.", color=TEXT)
        self.at("but it may hide")
        self.play(FadeIn(hidden), FadeIn(tag), Indicate(tree[3], color=GOLD), run_time=1.2)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Classification changes"
    TITLE = "The Molecule Behind the Tree"


class S02Shared(LivingScene):
    def construct(self):
        cells = VGroup(
            cell_icon(BAC, "Bacteria", at=[-4.25, 1.45, 0], scale=0.78),
            cell_icon(TEAL, "Archaea", at=[0, 1.45, 0], scale=0.78),
            cell_icon(EUK, "Eukarya", nucleus=True, at=[4.25, 1.45, 0], scale=0.78),
        )
        for i, c in enumerate(cells):
            bob(c, amp=0.06, speed=1.2 + i * 0.2, seed=i)
        self.at("To compare very different cells")
        self.play(LaggedStart(*[FadeIn(c, scale=0.85) for c in cells], lag_ratio=0.22), run_time=1.7)
        need = caption("Find the same record in every cell.", color=TEXT)
        self.at("scientists need the same kind")
        self.play(FadeIn(need), run_time=0.9)
        ribs = VGroup(*[chip("ribosome", GREY, 28).move_to([x, -0.25, 0]) for x in (-4.25, 0, 4.25)])
        self.at("Every cell builds proteins")
        self.play(FadeOut(need), LaggedStart(*[FadeIn(r, shift=UP * 0.2) for r in ribs], lag_ratio=0.18), run_time=1.5)
        strips = VGroup(*[rna_strip(TEXT, [x, -1.38, 0]) for x in (-4.25, 0, 4.25)])
        self.at("Ribosomal RNA forms")
        self.play(LaggedStart(*[TransformFromCopy(ribs[i], strips[i]) for i in range(3)], lag_ratio=0.18), run_time=1.7)
        conserved = VGroup(*[Rectangle(width=0.34, height=0.52, color=TEXT, fill_opacity=0.65).move_to(s[0].get_center() + LEFT * 0.65) for s in strips])
        self.at("Conserved parts let researchers")
        self.play(FadeIn(conserved), *[Indicate(c, color=TEXT) for c in conserved], run_time=1.5)
        differing = VGroup(*[Rectangle(width=0.34, height=0.52, color=col, fill_opacity=0.7).move_to(strips[i][0].get_center() + RIGHT * 0.62) for i, col in enumerate((BAC, TEAL, EUK))])
        ev = caption("Shared parts align; differences test ancestry.", color=TEXT)
        self.at("while differing parts")
        self.play(FadeIn(differing), FadeIn(ev), *[Indicate(d, color=d.get_color()) for d in differing], run_time=1.5)
        self.finish()


class S03Catalogues(LivingScene):
    def construct(self):
        strips = VGroup(rna_strip(TEXT, [-3.6, 2.55, 0]), rna_strip(TEXT, [-3.6, 1.55, 0]))
        tree = unresolved_tree(at=[4.2, 0.45, 0], scale=0.82)
        pulse(tree[3], base=2.5, amp=2.0, speed=2.0)
        self.at("Wose and Fox compared")
        self.play(FadeIn(strips), FadeIn(tree), run_time=1.4)
        top = tile_row([1] * 6, TEAL, at=[-3.6, 2.20, 0])
        bottom = tile_row([1] * 6, TEAL, at=[-3.6, 0.95, 0])
        self.at("Picture each catalog")
        self.play(ReplacementTransform(strips[0], top), ReplacementTransform(strips[1], bottom), run_time=1.8)
        tag = scope_tag("schematic")
        self.at("not a complete molecule")
        self.play(FadeIn(tag), run_time=0.8)
        links = VGroup(*[Line(top[i].get_bottom(), bottom[i].get_top(), color=TEXT, stroke_width=4) for i in range(5)])
        for link in links:
            link.layout_ok = True  # connector is intentionally anchored to its labelled tile
        self.at("Matching tiles pull")
        self.play(LaggedStart(*[Create(x) for x in links], lag_ratio=0.10),
                  bottom.animate.set_fill(opacity=0.38), run_time=1.8)
        few_bottom = tile_row([1, 0, 0, 1, 0, 0], BAC, at=[-3.6, -1.05, 0])
        few_links = VGroup(*[Line(top[i].get_bottom(), few_bottom[i].get_top(), color=TEXT, stroke_width=4) for i in (0, 3)])
        for link in few_links:
            link.layout_ok = True  # connector is intentionally anchored to its labelled tile
        self.at("Fewer matches leave")
        self.play(FadeIn(few_bottom), LaggedStart(*[Create(x) for x in few_links], lag_ratio=0.2), run_time=1.6)
        self.at("The pattern across pairs")
        self.play(links.animate.set_stroke(width=7), few_links.animate.set_stroke(width=7),
                  Indicate(tree[3], color=GOLD), run_time=1.5)
        self.finish()


class S04Predict(LivingScene):
    def construct(self):
        many = pair_diagram(5, TEXT, TEXT, at=[-3.35, 0.60, 0], width=4.7)
        few = pair_diagram(2, TEXT, TEXT, at=[3.35, 0.60, 0], width=4.7)
        bob(many, amp=0.07, speed=1.4)
        bob(few, amp=0.07, speed=1.2, seed=2)
        self.at("Here are hidden pairs")
        self.play(FadeIn(many, shift=DOWN * 0.2), FadeIn(few, shift=DOWN * 0.2), run_time=1.3)
        q1 = T("?", 48, GOLD, weight=BOLD).next_to(many, UP, buff=0.18)
        q2 = T("?", 48, GOLD, weight=BOLD).next_to(few, UP, buff=0.18)
        self.at("A pair shares many")
        self.play(FadeIn(q1), many.animate.scale(1.05), run_time=1.2)
        self.at("while another shares few")
        self.play(FadeIn(q2), few.animate.scale(1.05), run_time=1.2)
        q = question_card("Which pair should sit closer on the ancestry tree?", y=-3.08, size=30)
        self.at("Which pair should sit closer")
        self.play(FadeIn(q.question, shift=UP * 0.15), q1.animate.shift(RIGHT * 0.18), q2.animate.shift(LEFT * 0.18), run_time=1.4)
        self.at("Hold your answer")
        self.play(Indicate(q.question, color=GOLD), run_time=1.0)
        self.add(scope_tag("schematic"))
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Which pair should sit closer on the ancestry tree?"
    SECONDS = 4.5
    CARD = {"y": -3.08, "size": 30}

    def backdrop(self):
        return predict_backdrop()


class S06Reveal(LivingScene):
    def construct(self):
        tree = unresolved_tree(at=[4.45, 0.25, 0], scale=0.78)
        many = pair_diagram(5, TEAL, TEAL, at=[-3.25, 1.90, 0], width=4.45)
        moderate = pair_diagram(4, BAC, BAC, at=[-3.25, 0.05, 0], width=4.45)
        few = pair_diagram(2, TEAL, BAC, at=[-3.25, -1.80, 0], width=4.45)
        self.at("The pair with many shared pieces")
        self.play(FadeIn(many), FadeIn(tree), run_time=1.4)
        close = T("closer", 30, TEAL, weight=BOLD).next_to(many, RIGHT, buff=0.22)
        self.at("belongs closer")
        self.play(FadeIn(close), Indicate(tree[3], color=TEAL), run_time=1.1)
        self.at("The methane makers matched")
        self.play(FadeOut(close), FadeIn(moderate), many.animate.shift(RIGHT * 0.18), run_time=1.5)
        self.at("Typical bacteria also matched")
        self.play(FadeIn(few), moderate.animate.shift(RIGHT * 0.10), run_time=1.5)
        braces = VGroup(
            T("many", 26, TEAL).move_to([-0.55, 1.90, 0]),
            T("moderate", 26, BAC).move_to([-0.35, 0.05, 0]),
            T("few", 26, TEXT).move_to([-0.55, -1.80, 0]),
        )
        self.at("That repeated pattern")
        self.play(LaggedStart(*[FadeIn(x) for x in braces], lag_ratio=0.18),
                  Rotate(tree[3], angle=0.35), run_time=1.7)
        old = caption("one combined prokaryote branch?", color=GOLD)
        self.at("challenged a combined")
        self.play(FadeIn(old), Indicate(tree[3], color=GOLD), run_time=1.3)
        self.add(scope_tag("schematic"))
        self.finish()


class S06Claim(LivingScene):
    def construct(self):
        tree = tree_world(labels=False, at=[0, 0.30, 0], scale=0.95)
        joint = tree[1][1]
        bob(tree[2], amp=0.05, speed=1.2)
        self.at("A classification is a testable map")
        self.play(Create(tree[0]), FadeIn(tree[1]), FadeIn(tree[2]), run_time=1.8)
        tag = chip("ancestry claim", TEXT, 28).move_to([4.75, -1.55, 0])
        leader = Line(tag.get_left(), joint.get_center() + RIGHT * 0.18, color=TEXT, stroke_width=3)
        self.at("A branch claims")
        self.play(FadeIn(tag, shift=UP * 0.15), Create(leader), Indicate(joint, color=GOLD), run_time=1.2)
        evidence = VGroup(
            Arrow([-5.2, 0.8, 0], [-0.5, -0.55, 0], color=TEXT, stroke_width=5, tip_length=0.2),
            Arrow([5.2, 0.8, 0], [0.5, -0.55, 0], color=TEXT, stroke_width=5, tip_length=0.2),
            Arrow([0, 3.2, 0], [0, -0.25, 0], color=TEXT, stroke_width=5, tip_length=0.2),
        )
        self.at("When several comparisons")
        self.play(FadeOut(tag), FadeOut(leader), LaggedStart(*[GrowArrow(a) for a in evidence], lag_ratio=0.2), run_time=1.8)
        self.at("scientists redraw only")
        self.play(Rotate(tree[0][1], angle=-0.12, about_point=joint.get_center()),
                  Rotate(tree[0][2], angle=0.12, about_point=joint.get_center()), run_time=1.5)
        unchanged = caption("Same organisms. Better-supported map.", color=TEXT)
        self.at("The organisms themselves")
        self.play(FadeOut(evidence), FadeIn(unchanged), *[Indicate(x, color=x[0].get_color()) for x in tree[2]], run_time=1.4)
        self.finish()


class S07Domains(LivingScene):
    def construct(self):
        tree = tree_world(labels=False, at=[0, 0.05, 0], scale=0.92)
        self.at("The researchers interpreted this pattern")
        self.play(Create(tree[0]), FadeIn(tree[1]), FadeIn(tree[2]), run_time=1.8)
        labs = VGroup(
            T("Bacteria", 32, BAC, weight=BOLD).move_to([-3.25, 2.5, 0]),
            T("Archaea", 32, TEAL, weight=BOLD).move_to([0, 2.88, 0]),
            T("Eukarya", 32, EUK, weight=BOLD).move_to([3.25, 2.5, 0]),
        )
        self.at("Later the rank called domain")
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.12) for l in labs], lag_ratio=0.22), run_time=1.7)
        dates = VGroup(M("1977", 30, TEXT), Arrow(LEFT, RIGHT, color=GREY), M("1990", 30, TEXT)).arrange(RIGHT, buff=0.25).move_to([0, -2.82, 0])
        self.at("The methane makers joined")
        self.play(FadeIn(dates), Indicate(labs[1], color=TEAL), run_time=1.3)
        self.at("Their cells did not change")
        self.play(*[Indicate(x, color=x[0].get_color()) for x in tree[2]], run_time=1.3)
        cap = caption("Evidence changed the best-supported tree.", color=TEXT)
        self.at("The evidence changed")
        self.play(FadeOut(dates), run_time=0.5)
        self.play(FadeIn(cap), tree[1][1].animate.set_color(GOLD), run_time=0.9)
        self.finish()


class S07Evidence(LivingScene):
    def construct(self):
        tree = tree_world(labels=False, at=[0, 0.60, 0], scale=0.65)
        self.add(tree)
        cards = VGroup(
            chip("structure", TEXT, 28).move_to([-4.75, 2.25, 0]),
            chip("development", TEXT, 28).move_to([-4.75, 0.75, 0]),
            chip("RNA", TEXT, 28).move_to([4.75, 2.25, 0]),
            chip("DNA", TEXT, 28).move_to([4.75, 0.75, 0]),
        )
        self.at("Molecular evidence does not automatically")
        self.play(FadeIn(cards[2]), FadeIn(cards[3]), tree.animate.set_opacity(0.72), run_time=1.4)
        self.at("It adds a comparison")
        self.play(FadeIn(cards[0]), cards[2].animate.shift(LEFT * 0.35), run_time=1.2)
        self.at("Strong classifications weigh")
        self.play(FadeIn(cards[1]), cards[3].animate.shift(LEFT * 0.35), run_time=1.4)
        agree = VGroup(cards[0].copy(), cards[2].copy(), cards[3].copy()).arrange(DOWN, buff=0.15).scale(0.78).move_to([-4.6, -1.55, 0])
        self.at("Agreement strengthens")
        self.play(TransformFromCopy(VGroup(cards[0], cards[2], cards[3]), agree),
                  tree[1][1].animate.set_color(TEXT), run_time=1.5)
        conflict = T("?", 58, GOLD, weight=BOLD).move_to([4.65, -1.55, 0])
        self.at("Conflict shows")
        self.play(ReplacementTransform(cards[1].copy(), conflict),
                  conflict.animate.shift(LEFT * 0.35), run_time=1.4)
        self.finish()


class S08Limits(LivingScene):
    def construct(self):
        tree = tree_world(labels=True, model_tag=True, at=[0, 0.25, 0], scale=0.78)
        tree[-1].move_to([4.2, -1.85, 0])
        self.add(tree)
        percent = M("% DNA", 44, GREY).move_to([-4.5, 1.2, 0])
        clock = VGroup(Circle(radius=0.48, color=GREY, stroke_width=4),
                       Line(ORIGIN, UP * 0.29, color=GREY, stroke_width=4),
                       Line(ORIGIN, RIGHT * 0.25, color=GREY, stroke_width=4)).move_to([4.7, 2.45, 0])
        self.at("The overlap scores are not")
        self.play(FadeIn(percent, shift=RIGHT * 0.2), run_time=1.1)
        self.at("They do not tell when")
        self.play(FadeIn(clock, shift=LEFT * 0.2), percent.animate.shift(LEFT * 0.2).set_opacity(0.35), run_time=1.2)
        summary = caption("Scores summarize shared RNA catalogue pieces.", color=TEXT)
        self.at("They summarize shared pieces")
        self.play(FadeOut(percent), FadeOut(clock), FadeIn(summary), run_time=1.3)
        cards = VGroup(chip("more organisms", TEXT, 26), chip("other genes", TEXT, 26), chip("membranes", TEXT, 26)).arrange(RIGHT, buff=0.35).move_to([0, -2.72, 0])
        self.at("A tree remains a claim")
        self.play(FadeOut(summary), tree[1][1].animate.set_color(GOLD), run_time=1.2)
        self.at("tested against more organisms")
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cards], lag_ratio=0.22), run_time=1.7)
        self.at("any evidence that can challenge")
        self.play(cards.animate.shift(UP * 0.18), Indicate(tree[1][1], color=TEXT), run_time=1.4)
        self.finish()


class S09Close(LivingScene):
    def construct(self):
        tree = tree_world(labels=True, model_tag=False, at=[0, 0.25, 0], scale=0.82)
        self.at("That is why changing a group")
        self.play(FadeIn(tree), run_time=1.5)
        cabinet = VGroup(
            RoundedRectangle(corner_radius=0.18, width=4.0, height=4.7, color=GREY, stroke_width=5, fill_color=GREY, fill_opacity=0.10),
            *[Line([-1.8, y, 0], [1.8, y, 0], color=GREY, stroke_width=4) for y in (-0.78, 0.78)],
            *[T("fixed", 28, GREY).move_to([0, y, 0]) for y in (-1.55, 0, 1.55)],
        ).move_to([0, 0.25, 0])
        self.at("Classification is a model")
        self.play(ReplacementTransform(tree, cabinet), run_time=1.5)
        self.at("not a permanent filing cabinet")
        new_tree = tree_world(labels=True, model_tag=True, at=[0, 0.25, 0], scale=0.82)
        self.play(ReplacementTransform(cabinet, new_tree), run_time=1.6)
        evidence = Arrow([-5.4, 0.3, 0], [-0.45, -0.35, 0], color=TEXT, stroke_width=7, tip_length=0.25)
        self.at("When stronger evidence")
        self.play(GrowArrow(evidence), new_tree[1][1].animate.set_color(GOLD), run_time=1.5)
        limits = chip("limits visible", TEXT, 26).move_to([4.85, -2.75, 0])
        self.at("while keeping its limits visible")
        self.play(FadeIn(limits), FadeOut(evidence), Indicate(new_tree[1][1], color=TEXT), run_time=1.4)
        self.finish()


class S10End(EndCard):
    LINE = "Classification changes when new evidence changes\nthe best-supported picture of ancestry."
