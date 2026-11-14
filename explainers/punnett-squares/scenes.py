"""Where the White Was Hiding — Punnett-square explainer.

COLOR MAP (kept for the whole film)
  PURPLE: dominant P allele and purple flowers
  WHITE:  recessive p allele and white flowers
  GREEN:  Punnett grid
  YELLOW: probability and chance
  BLUE:   neutral teaching labels

The pea plant, allele cards, and Punnett square are each built by one shared
function so carried pictures keep exactly the same scale and position.
"""
from bp_parts import *  # noqa: F401,F403


PURPLE = "#B58CD9"
WHITE = "#FFFFFF"
PALE_BLUE = BLUE


def allele(letter, color, size=0.9):
    """One allele card; the letter is deliberately inside its own card."""
    box = RoundedRectangle(corner_radius=0.14, width=size, height=size,
                           stroke_color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.20)
    label = M(letter, max(28, int(size * 44)), color, weight=BOLD).move_to(box)
    return VGroup(box, label)


def flower(color=PURPLE, scale=1.0):
    """A simple, non-botanical flower icon used consistently throughout."""
    petals = VGroup(*[
        Circle(radius=0.34, stroke_width=2.5, stroke_color=color,
               fill_color=color, fill_opacity=0.82).move_to(
                   0.42 * np.array([np.cos(a), np.sin(a), 0]))
        for a in np.linspace(0, TAU, 5, endpoint=False)
    ])
    center = Circle(radius=0.22, color=YELLOW, fill_color=YELLOW,
                    fill_opacity=0.95, stroke_width=2)
    g = VGroup(petals, center).scale(scale)
    g.layout_ok = True  # purely pictorial icon: no text for the layout checker
    return g


def plant(color=PURPLE, at=ORIGIN, scale=1.0, sway=False):
    """The carried pea-plant picture."""
    stem = Line(DOWN * 1.25, UP * 0.25, color=GREEN, stroke_width=9)
    leaf_l = Ellipse(width=0.75, height=0.34, color=GREEN,
                     fill_color=GREEN, fill_opacity=0.75).rotate(0.45).move_to([-0.38, -0.55, 0])
    leaf_r = leaf_l.copy().flip(UP).move_to([0.38, -0.82, 0])
    bloom = flower(color, 0.82).move_to([0, 0.72, 0])
    g = VGroup(stem, leaf_l, leaf_r, bloom).scale(scale).move_to(at)
    g.bloom = bloom
    # Plant motion is supplied by the scene's growth/transform beats. Avoid a
    # permanent updater on every plant; a family row can otherwise redraw
    # dozens of vector petals every frame.
    g.layout_ok = True
    return g


def family_world(show_descendant=True):
    """The opening family timeline, rebuilt unchanged for the title."""
    p1 = plant(PURPLE, [-4.7, 0.45, 0], 0.9, True)
    p2 = plant(WHITE, [-2.1, 0.45, 0], 0.9, True)
    kids = VGroup(*[plant(PURPLE, [x, 0.35, 0], 0.65, True) for x in (0.25, 1.75, 3.25)])
    desc = plant(WHITE, [5.0, 0.35, 0], 0.72, True)
    arrows = VGroup(
        Arrow([-1.2, 0.4, 0], [-0.35, 0.4, 0], buff=0.05, color=GREY, stroke_width=4),
        Arrow([3.9, 0.4, 0], [4.3, 0.4, 0], buff=0.05, color=GREY, stroke_width=4),
    )
    g = VGroup(p1, p2, kids, arrows)
    if show_descendant:
        g.add(desc)
    g.purple_parent, g.white_parent, g.kids, g.descendant = p1, p2, kids, desc
    return g


def pair_cards(genotype="Pp", at=(0, 0, 0), size=1.0):
    cards = VGroup(*[
        allele(ch, PURPLE if ch == "P" else WHITE, size)
        for ch in genotype
    ]).arrange(RIGHT, buff=0.22).move_to(at)
    return cards


def plant_with_pair(genotype="Pp", at=(0, -0.55, 0), scale=1.35):
    col = PURPLE if "P" in genotype else WHITE
    pl = plant(col, at, scale, True)
    cards = pair_cards(genotype, [at[0], at[1] - 0.35, 0], 0.72)
    return VGroup(pl, cards)


def square_world(blank=False, flowers=False, probabilities=False, center=(0.5, 0.15, 0), cell=2.05):
    """The one canonical Pp × Pp square used from pairing through counting."""
    cx, cy, _ = center
    boxes = VGroup()
    box_map = {}
    for row in range(2):
        for col in range(2):
            b = Square(cell, stroke_color=GREEN, stroke_width=5,
                       fill_color=GREEN, fill_opacity=0.07)
            b.move_to([cx + (col - 0.5) * cell, cy + (0.5 - row) * cell, 0])
            boxes.add(b)
            box_map[(row, col)] = b
    top = VGroup(allele("P", PURPLE, 0.7), allele("p", WHITE, 0.7))
    top.arrange(RIGHT, buff=cell - 0.7).move_to([cx, cy + cell + 0.55, 0])
    side = VGroup(allele("P", PURPLE, 0.7), allele("p", WHITE, 0.7))
    side.arrange(DOWN, buff=cell - 0.7).move_to([cx - cell - 0.55, cy, 0])
    g = VGroup(boxes, top, side)
    g.boxes, g.top_cards, g.side_cards, g.box_map = boxes, top, side, box_map
    names = {(0, 0): "PP", (0, 1): "Pp", (1, 0): "Pp", (1, 1): "pp"}
    if blank:
        marks = VGroup(*[T("?", 48, YELLOW, weight=BOLD).move_to(box_map[k]) for k in names])
        g.add(marks)
        g.marks = marks
    else:
        labs = VGroup(*[M(names[k], 42, TEXT, weight=BOLD).move_to(box_map[k]) for k in names])
        g.add(labs)
        g.genotypes = labs
    if probabilities:
        probs = VGroup(*[M("1/4", 25, YELLOW).move_to(box_map[k].get_corner(UR) + DL * 0.36)
                         for k in names])
        g.add(probs)
        g.probabilities = probs
    if flowers:
        blooms = VGroup()
        for k in names:
            col = WHITE if k == (1, 1) else PURPLE
            blooms.add(flower(col, 0.40).move_to(box_map[k].get_center() + DOWN * 0.48))
        if hasattr(g, "genotypes"):
            for lab in g.genotypes:
                lab.shift(UP * 0.43)
        g.add(blooms)
        g.blooms = blooms
    return g


def prediction_backdrop():
    return square_world(blank=True)


class S00Hook(SpokenScene):
    def construct(self):
        parents = family_world(False)
        labels = VGroup(
            T("true-breeding", 28, PALE_BLUE).move_to([-4.7, -1.5, 0]),
            T("purple", 28, PURPLE).move_to([-4.7, -1.95, 0]),
            T("white", 28, WHITE).move_to([-2.1, -1.75, 0]),
        )
        self.play(LaggedStart(FadeIn(parents.purple_parent, shift=RIGHT),
                              FadeIn(parents.white_parent, shift=LEFT), lag_ratio=0.25), run_time=1.2)
        self.at("white flowers disappear")
        self.play(FadeIn(labels), run_time=0.8)
        self.at("gives only purple offspring")
        self.play(GrowArrow(parents[3][0]), LaggedStart(*[GrowFromPoint(k, [-0.3, 0.4, 0]) for k in parents.kids],
                                                       lag_ratio=0.22), run_time=2.1)
        self.at("white flowers return")
        descendant = parents.descendant
        self.play(GrowArrow(parents[3][1]), GrowFromCenter(descendant), run_time=1.2)
        question = T("?", 76, YELLOW, weight=BOLD).move_to([5.0, 2.55, 0])
        bob(question, amp=0.12, speed=1.7)
        self.play(FadeIn(question, scale=1.4), run_time=0.7)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Punnett Squares"
    TITLE = "Where the White Was Hiding"


class S02Alleles(SpokenScene):
    def construct(self):
        pl = plant(PURPLE, [0, -1.15, 0], 1.75, True)
        self.play(GrowFromCenter(pl), run_time=1.0)
        self.at("different versions")
        gene = chip("flower-color gene", PALE_BLUE, 30).move_to([0, 3.3, 0])
        self.play(FadeIn(gene, shift=DOWN * 0.15), run_time=0.7)
        self.at("called alleles")
        cards = pair_cards("Pp", [0, 1.55, 0], 1.0).arrange(RIGHT, buff=0.7).move_to([0, 1.55, 0])
        self.play(TransformFromCopy(gene, cards), run_time=1.2)
        labels = VGroup(T("purple allele", 28, PURPLE), T("white allele", 28, WHITE))
        labels[0].next_to(cards[0], LEFT, buff=0.35)
        labels[1].next_to(cards[1], RIGHT, buff=0.35)
        self.at("track a purple allele")
        self.play(FadeIn(labels[0]), Indicate(cards[0], color=PURPLE), run_time=0.7)
        self.at("and a white allele")
        self.play(FadeIn(labels[1]), Indicate(cards[1], color=WHITE), run_time=0.7)
        self.at("carries a pair")
        pair_label = T("pair", 30, PALE_BLUE, weight=BOLD).next_to(cards, UP, buff=0.18)
        self.play(FadeIn(pair_label), cards.animate.set_x(0), run_time=0.7)
        self.finish()


class S02Parents(SpokenScene):
    def construct(self):
        left = plant_with_pair("PP", [-3.7, 0.1, 0], 1.35)
        right = plant_with_pair("pp", [3.7, 0.1, 0], 1.35)
        self.play(FadeIn(left, shift=RIGHT), run_time=0.9)
        self.at("only purple alleles")
        self.play(Indicate(left[1], color=PURPLE), run_time=0.7)
        self.at("white parent")
        self.play(FadeIn(right, shift=LEFT), run_time=0.9)
        self.at("only white alleles")
        self.play(Indicate(right[1], color=WHITE), run_time=0.7)
        child = plant(PURPLE, [0, -0.35, 0], 1.28, True)
        p_card = left[1][0].copy()
        w_card = right[1][0].copy()
        self.at("received one allele")
        self.play(GrowFromCenter(child), p_card.animate.move_to([-0.46, -0.7, 0]), run_time=1.0)
        self.at("from each parent")
        self.play(w_card.animate.move_to([0.46, -0.7, 0]), run_time=1.0)
        offspring = T("offspring: Pp", 32, PALE_BLUE, weight=BOLD).move_to([0, 2.75, 0])
        self.play(FadeIn(offspring), run_time=0.6)
        self.finish()


class S03Genotype(SpokenScene):
    def construct(self):
        pl = plant(PURPLE, [0, -0.6, 0], 1.8, True)
        cards = pair_cards("Pp", [0, -1.25, 0], 1.0)
        self.play(FadeIn(pl), FadeIn(cards), run_time=0.8)
        self.at("is the genotype")
        gl = T("genotype: Pp", 36, PALE_BLUE, weight=BOLD).move_to([-3.5, 2.5, 0])
        self.play(FadeIn(gl), Circumscribe(cards, color=PALE_BLUE), run_time=0.9)
        self.at("is the phenotype")
        ph = T("phenotype: purple", 36, PURPLE, weight=BOLD).move_to([3.25, 2.5, 0])
        self.play(FadeIn(ph), Circumscribe(pl.bloom, color=PURPLE), run_time=0.9)
        self.at("still carries white")
        ring = SurroundingRectangle(cards[1], color=YELLOW, buff=0.1, stroke_width=5)
        pulse(ring, base=5, amp=1.5, speed=3)
        self.play(Create(ring), cards[1].animate.shift(UP * 0.12), run_time=0.7)
        self.finish()


class S03Terms(SpokenScene):
    def construct(self):
        cards = VGroup(pair_cards("PP", [-4.2, 0.55, 0], 1.05),
                       pair_cards("Pp", [0, 0.55, 0], 1.05),
                       pair_cards("pp", [4.2, 0.55, 0], 1.05))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cards], lag_ratio=0.22), run_time=1.2)
        self.at("are homozygous")
        homo = T("homozygous", 34, PALE_BLUE, weight=BOLD).move_to([0, 2.6, 0])
        links = VGroup(Line([-4.2, 1.35, 0], [-1.6, 2.28, 0], color=PALE_BLUE, stroke_width=3),
                       Line([4.2, 1.35, 0], [1.6, 2.28, 0], color=PALE_BLUE, stroke_width=3))
        self.play(Create(links), FadeIn(homo), run_time=1.0)
        self.at("is heterozygous")
        het = T("heterozygous", 34, YELLOW, weight=BOLD).move_to([0, -0.55, 0])
        self.play(FadeIn(het), Indicate(cards[1], color=YELLOW), run_time=0.9)
        self.at("first generation plants")
        pl = plant(PURPLE, [0, -2.15, 0], 0.78, True)
        self.play(cards[1].animate.scale(0.7).move_to([0, -2.45, 0]), GrowFromCenter(pl),
                  FadeOut(links), FadeOut(homo), FadeOut(cards[0]), FadeOut(cards[2]), run_time=1.3)
        self.at("white allele stays present")
        self.play(Indicate(cards[1][1], color=WHITE), run_time=0.8)
        self.finish()


class S04Dominance(SpokenScene):
    def construct(self):
        panels = VGroup()
        data = [("PP", PURPLE, -4.2), ("Pp", PURPLE, 0), ("pp", WHITE, 4.2)]
        for geno, col, x in data:
            frame = RoundedRectangle(width=3.4, height=5.4, corner_radius=0.2,
                                     stroke_color=GREY, stroke_width=2).move_to([x, 0, 0])
            pair = pair_cards(geno, [x, 1.35, 0], 0.9)
            bloom = flower(col, 0.95).move_to([x, -0.75, 0])
            panels.add(VGroup(frame, pair, bloom))
        self.play(LaggedStart(*[FadeIn(p) for p in panels], lag_ratio=0.2), run_time=1.3)
        self.at("purple allele is dominant")
        dom = T("dominant P", 34, PURPLE, weight=BOLD).move_to([0, 3.15, 0])
        self.play(FadeIn(dom), Indicate(VGroup(panels[0], panels[1]), color=PURPLE), run_time=1.0)
        self.at("one copy makes purple")
        cover = panels[1][1][0].copy().set_opacity(0.35).move_to(panels[1][1][1])
        cover.layout_ok = True  # deliberate dominant-P overlay on the recessive card
        self.play(FadeIn(cover), panels[1][2].animate.scale(1.08), run_time=0.8)
        self.at("white allele is recessive")
        rec = T("recessive p", 34, WHITE, weight=BOLD).move_to([4.2, 3.15, 0])
        self.play(FadeIn(rec), Indicate(panels[2][1], color=WHITE), run_time=0.8)
        note = scope_tag("complete dominance in this pea model", 24, GREY)
        self.at("no purple allele")
        self.play(FadeIn(note), Circumscribe(panels[2][2], color=WHITE), run_time=0.8)
        self.finish()


class S04Common(SpokenScene):
    def construct(self):
        subject = plant_with_pair("Pp", [0, -0.25, 0], 1.55)
        self.play(FadeIn(subject), run_time=0.8)
        bad = VGroup(chip("common", GREY, 30), chip("stronger", GREY, 30), chip("passed on more", GREY, 30))
        bad.arrange(DOWN, buff=0.35).move_to([-4.25, 0.2, 0])
        self.at("does not mean common")
        self.play(FadeIn(bad[0]), run_time=0.45)
        self.at("stronger")
        self.play(FadeIn(bad[1]), run_time=0.45)
        self.at("passed on")
        self.play(FadeIn(bad[2]), run_time=0.45)
        strikes = VGroup(*[Line(b.get_corner(DL), b.get_corner(UR), color=RED, stroke_width=7) for b in bad])
        strikes.layout_ok = True  # deliberate strike-throughs of the three misconceptions
        for strike in strikes:
            strike.layout_ok = True
        self.play(LaggedStart(*[Create(s) for s in strikes], lag_ratio=0.2), run_time=1.0)
        self.at("which phenotype appears")
        answer = T("phenotype with a mixed pair", 32, PURPLE, weight=BOLD).move_to([3.05, 2.55, 0])
        arrow = Arrow([3.0, 2.15, 0], [1.0, 0.85, 0], color=PURPLE, stroke_width=5)
        self.play(FadeOut(bad), FadeOut(strikes), FadeIn(answer), GrowArrow(arrow), run_time=1.0)
        self.finish()


class S05Separate(SpokenScene):
    def construct(self):
        cell = RoundedRectangle(width=3.6, height=2.2, corner_radius=0.5,
                                color=GREY, stroke_width=4, fill_color=GREY, fill_opacity=0.08).move_to([0, 2, 0])
        pair = pair_cards("Pp", [0, 2, 0], 1.0)
        self.play(FadeIn(cell), FadeIn(pair), run_time=0.9)
        self.at("pair separates")
        streams = VGroup(*[Circle(radius=0.62, color=GREY, fill_color=GREY, fill_opacity=0.08)
                           .move_to([x, -0.3, 0]) for x in (-3.7, 3.7)])
        self.play(FadeIn(streams), pair[0].animate.move_to(streams[0]),
                  pair[1].animate.move_to(streams[1]), run_time=1.5)
        self.at("during meiosis")
        seg = T("segregation", 36, PALE_BLUE, weight=BOLD).move_to([0, 0.25, 0])
        self.play(FadeIn(seg), FadeOut(cell), run_time=0.7)
        self.at("both kinds")
        flow = VGroup()
        for row in range(2):
            for col, ch in enumerate("PpPpPp"):
                x = -5.0 + col * 2.0
                y = -1.55 - row * 1.05
                c = Circle(radius=0.38, color=GREY, fill_color=GREY, fill_opacity=0.08).move_to([x, y, 0])
                a = allele(ch, PURPLE if ch == "P" else WHITE, 0.48).move_to(c)
                flow.add(VGroup(c, a))
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.35) for c in flow], lag_ratio=0.07), run_time=1.6)
        self.at("about equal numbers")
        halves = VGroup(T("P: about half", 30, PURPLE), T("p: about half", 30, WHITE))
        halves.arrange(RIGHT, buff=1.3).move_to([0, -3.25, 0])
        self.play(FadeIn(halves), run_time=0.7)
        self.finish()


class S06Pairing(SpokenScene):
    def construct(self):
        cells_top = VGroup(allele("P", PURPLE, 0.72), allele("p", WHITE, 0.72))
        cells_top.arrange(RIGHT, buff=1.35).move_to([0.5, 2.9, 0])
        cells_side = VGroup(allele("P", PURPLE, 0.72), allele("p", WHITE, 0.72))
        cells_side.arrange(DOWN, buff=1.35).move_to([-3.15, 0.15, 0])
        self.play(FadeIn(cells_top, shift=DOWN), FadeIn(cells_side, shift=RIGHT), run_time=1.1)
        self.at("from each parent")
        meet = Dot([0.5, 0.15, 0], radius=0.22, color=YELLOW)
        moving_top, moving_side = cells_top[0].copy(), cells_side[0].copy()
        moving_top.layout_ok = moving_side.layout_ok = True
        self.add(moving_top, moving_side)
        self.play(moving_top.animate.move_to(meet), moving_side.animate.move_to(meet), run_time=1.0)
        self.at("matter of chance")
        self.play(FadeOut(moving_top), FadeOut(moving_side), FadeIn(meet),
                  Flash(meet, color=YELLOW, line_length=0.45), run_time=0.8)
        self.at("grid can organize")
        world = square_world(blank=True)
        self.play(FadeOut(meet), Create(world.boxes),
                  Transform(cells_top, world.top_cards), Transform(cells_side, world.side_cards), run_time=1.6)
        self.at("every possible pairing")
        self.play(LaggedStart(*[FadeIn(m, scale=1.4) for m in world.marks], lag_ratio=0.12), run_time=1.1)
        self.finish()


class S06Probability(SpokenScene):
    def construct(self):
        world = square_world(blank=False)
        self.add(world.boxes, world.top_cards, world.side_cards)
        self.at("equally often")
        halves = VGroup(M("1/2", 30, YELLOW).next_to(world.top_cards, UP, buff=0.15),
                        M("1/2", 30, YELLOW).next_to(world.side_cards, LEFT, buff=0.15))
        self.play(FadeIn(halves), Indicate(world.top_cards, color=YELLOW),
                  Indicate(world.side_cards, color=YELLOW), run_time=1.0)
        self.at("every box")
        self.play(LaggedStart(*[b.animate.set_fill(YELLOW, opacity=0.15) for b in world.boxes], lag_ratio=0.12), run_time=1.4)
        self.at("same probability")
        probs = VGroup(*[M("1/4", 28, YELLOW).move_to(b) for b in world.boxes])
        self.play(LaggedStart(*[FadeIn(p, scale=1.25) for p in probs], lag_ratio=0.12), run_time=1.2)
        self.at("probability map")
        title = T("probability map", 38, YELLOW, weight=BOLD).move_to([4.65, 2.85, 0])
        self.play(FadeIn(title), world.boxes.animate.set_stroke(YELLOW), run_time=0.9)
        self.finish()


class S07Predict(SpokenScene):
    def construct(self):
        world = prediction_backdrop()
        self.add(world.boxes)
        self.at("either allele")
        self.play(FadeIn(world.top_cards, shift=DOWN), FadeIn(world.side_cards, shift=RIGHT), run_time=1.0)
        self.at("Predict which pairing")
        self.play(LaggedStart(*[FadeIn(m, scale=1.3) for m in world.marks], lag_ratio=0.12), run_time=1.0)
        q = question_card("Which pairing can make a white plant?", y=-3.15, size=32, max_w=10.8)
        self.at("make a white plant")
        self.play(FadeIn(q.question), run_time=0.7)
        self.at("before the flowers appear")
        self.play(Indicate(VGroup(world.top_cards, world.side_cards), color=YELLOW), run_time=1.0)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "Which pairing can make a white plant?"
    SECONDS = 4.5
    CARD = {"y": -3.15, "size": 32, "max_w": 10.8}

    def backdrop(self):
        return prediction_backdrop()


class S09Reveal(SpokenScene):
    def construct(self):
        blank = prediction_backdrop()
        self.add(blank.boxes, blank.top_cards, blank.side_cards, blank.marks)
        self.play(Indicate(blank.marks, color=YELLOW, scale_factor=1.25), run_time=1.2)
        self.play(blank.boxes.animate.set_stroke(YELLOW, width=6), run_time=0.6)
        self.play(blank.boxes.animate.set_stroke(GREEN, width=4), run_time=0.6)
        self.at("small pea arrives")
        self.play(blank.top_cards[1].animate.shift(DOWN * 0.18),
                  blank.side_cards[1].animate.shift(RIGHT * 0.18), run_time=0.9)
        world = square_world(blank=False, flowers=True)
        self.play(FadeOut(blank.marks), LaggedStart(*[FadeIn(g, scale=0.8) for g in world.genotypes],
                                                   lag_ratio=0.13), run_time=1.4)
        self.at("from both parents")
        ring = SurroundingRectangle(world.box_map[(1, 1)], color=YELLOW, buff=0.08, stroke_width=6)
        self.play(Create(ring), FadeIn(world.blooms[3], scale=0.5), run_time=1.0)
        self.at("other pairings")
        self.play(LaggedStart(*[FadeIn(world.blooms[i], scale=0.5) for i in range(3)], lag_ratio=0.15), run_time=1.2)
        self.at("flowers are purple")
        self.play(Indicate(VGroup(*world.blooms[:3]), color=PURPLE), run_time=0.9)
        self.finish()


class S10Read(SpokenScene):
    def construct(self):
        world = square_world(blank=False, flowers=True, center=(0.5, 0.85, 0), cell=1.65)
        self.add(world)
        self.at("genotype before phenotype")
        geno = VGroup(M("1 PP", 32, TEXT), M(":", 32, GREY), M("2 Pp", 32, TEXT),
                      M(":", 32, GREY), M("1 pp", 32, TEXT)).arrange(RIGHT, buff=0.22)
        geno.move_to([0.5, -1.55, 0])
        self.play(LaggedStart(*[FadeIn(x) for x in geno], lag_ratio=0.12), run_time=1.2)
        self.at("three groups")
        self.play(Indicate(geno, color=YELLOW), run_time=0.8)
        self.at("combines the first two")
        bar = VGroup(
            Rectangle(width=7.5, height=0.82, fill_color=PURPLE, fill_opacity=0.75,
                      stroke_color=PURPLE).move_to([-1.0, -2.85, 0]),
            Rectangle(width=2.5, height=0.82, fill_color=WHITE, fill_opacity=0.85,
                      stroke_color=WHITE).move_to([4.0, -2.85, 0]),
        )
        self.play(GrowFromEdge(bar[0], LEFT), run_time=1.0)
        self.at("same purple phenotype")
        labels = VGroup(T("3 purple", 30, BG, weight=BOLD).move_to(bar[0]),
                        T("1 white", 30, BG, weight=BOLD).move_to(bar[1]))
        labels.layout_ok = True  # dark labels are intentionally placed inside their ratio bars
        self.play(GrowFromEdge(bar[1], LEFT), FadeIn(labels), run_time=0.9)
        self.finish()


class S10Count(SpokenScene):
    def construct(self):
        world = square_world(blank=False, flowers=True, center=(-3.3, 0.7, 0), cell=1.45)
        self.add(world)
        geno = M("1 PP : 2 Pp : 1 pp", 28, TEXT).move_to([-3.3, -1.65, 0])
        pheno = M("3 purple : 1 white", 28, TEXT).move_to([-3.3, -2.35, 0])
        self.at("genotype pattern")
        self.play(FadeIn(geno), Indicate(world.genotypes, color=YELLOW), run_time=0.9)
        self.at("visible color")
        self.play(FadeIn(pheno), Indicate(world.blooms, color=YELLOW), run_time=0.9)
        def count_panel(total, white):
            box = RoundedRectangle(width=3.4, height=2.05, corner_radius=0.16,
                                   stroke_color=GREY, stroke_width=2.5,
                                   fill_color=BG, fill_opacity=0.9).move_to([4.25, 1.5, 0])
            title = T("running batch", 24, GREY).move_to([4.25, 2.15, 0])
            rows = VGroup(M(f"offspring = {total:2d}", 28, TEXT),
                          M(f"white     = {white:2d}", 28, WHITE))
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.25, 1.35, 0])
            return VGroup(box, title, rows)
        read = count_panel(0, 0)
        self.at("across repeated offspring")
        self.play(FadeIn(read), run_time=0.7)
        icons = VGroup()
        colors = [PURPLE, PURPLE, WHITE, PURPLE, PURPLE, PURPLE, PURPLE, WHITE,
                  PURPLE, PURPLE, PURPLE, WHITE]
        for i, col in enumerate(colors):
            icon = flower(col, 0.24).move_to([2.5 + (i % 4) * 1.15, -0.25 - (i // 4) * 0.9, 0])
            icons.add(icon)
        mid = count_panel(12, 2)
        final = count_panel(40, 11)
        self.play(LaggedStart(*[FadeIn(i, shift=LEFT * 0.25) for i in icons[:6]], lag_ratio=0.09),
                  ReplacementTransform(read, mid), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(i, shift=LEFT * 0.25) for i in icons[6:]], lag_ratio=0.09),
                  ReplacementTransform(mid, final), run_time=1.3)
        self.finish()


class S11Chance(SpokenScene):
    def construct(self):
        f = ValueTracker(0.25)
        wheel = dial(f, center=[-3.8, 1.0, 0], radius=1.55, label="each box", color=YELLOW)
        wheel.update()
        for mob in wheel.get_family():
            mob.clear_updaters()
        self.play(FadeIn(wheel), run_time=0.9)
        self.at("not four promised offspring")
        promised = T("4 boxes ≠ 4 promised offspring", 34, TEXT, weight=BOLD).move_to([1.9, 2.8, 0])
        self.play(FadeIn(promised), run_time=0.8)
        left = VGroup(*[flower(PURPLE, 0.42) for _ in range(4)]).arrange(RIGHT, buff=0.45).move_to([2.1, 0.7, 0])
        self.at("may miss white entirely")
        self.play(LaggedStart(*[GrowFromCenter(x) for x in left], lag_ratio=0.16), run_time=1.4)
        lab1 = T("all purple — possible", 28, PALE_BLUE).next_to(left, DOWN, buff=0.22)
        self.play(FadeIn(lab1), run_time=0.5)
        mixed_cols = [PURPLE, WHITE, PURPLE, WHITE]
        right = VGroup(*[flower(c, 0.42) for c in mixed_cols]).arrange(RIGHT, buff=0.45).move_to([2.1, -1.75, 0])
        self.at("may contain several")
        self.play(LaggedStart(*[GrowFromCenter(x) for x in right], lag_ratio=0.16), run_time=1.4)
        lab2 = T("several white — possible", 28, PALE_BLUE).next_to(right, DOWN, buff=0.22)
        tag = scope_tag("schematic", 24, GREY)
        self.play(FadeIn(lab2), FadeIn(tag), run_time=0.5)
        self.finish()


class S12Rule(SpokenScene):
    def construct(self):
        start = pair_cards("Pp", [-4.8, 1.0, 0], 0.9)
        cells = VGroup(Circle(radius=0.58, color=GREY).move_to([-2.2, 2.0, 0]),
                       Circle(radius=0.58, color=GREY).move_to([-2.2, 0.0, 0]))
        self.play(FadeIn(start), run_time=0.7)
        # Kokoro alignment transcribes the spoken "alleles" as "Aleals" here.
        self.at("Aleals separate")
        self.play(FadeIn(cells), start[0].animate.move_to(cells[0]),
                  start[1].animate.move_to(cells[1]), run_time=1.2)
        self.at("meet by chance")
        meet = pair_cards("Pp", [0, 1.0, 0], 0.75)
        arrows = VGroup(Arrow([-1.5, 1.9, 0], [-0.7, 1.25, 0], color=YELLOW),
                       Arrow([-1.5, 0.1, 0], [-0.7, 0.75, 0], color=YELLOW))
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), FadeIn(meet), run_time=1.1)
        self.at("square organizes")
        grid = square_world(blank=False, center=(3.7, 0.8, 0), cell=1.25)
        self.play(Create(grid.boxes), FadeIn(grid.genotypes), FadeIn(grid.top_cards),
                  FadeIn(grid.side_cards), run_time=1.4)
        self.at("does not promise")
        marker = Dot(grid.box_map[(1, 1)].get_center(), radius=0.15, color=YELLOW)
        loop = CurvedArrow(grid.box_map[(1, 1)].get_bottom(), [1.2, -2.4, 0], angle=-1.2,
                           color=YELLOW, stroke_width=5)
        empty = flower(GREY, 0.55).set_opacity(0.35).move_to([0, -2.5, 0])
        self.play(FadeIn(marker), Create(loop), FadeIn(empty), run_time=1.0)
        self.at("which offspring")
        self.play(MoveAlongPath(marker, loop), empty.animate.set_opacity(0.8), run_time=1.2)
        self.finish()


class S13End(EndCard):
    LINE = "Allele separation creates inheritance chances;\nPunnett squares organize, not guarantee, outcomes."
