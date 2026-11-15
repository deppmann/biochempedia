"""From a Programmed Cut to a Tested Knockout.

COLOR MAP (shared across the chapter pair)
  PURPLE = chosen gene and repaired alleles
  BLUE   = guide RNA
  GOLD   = Cas9
  ORANGE = PAM
  GREEN  = phenotype, function, and assay readouts
  GREY   = uncertainty, mixed outcomes, and neutral structure

All pictures are schematic blocks and cartoons, never molecular structures.
"""
from bp_parts import *  # noqa: F401,F403


PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def arrow_between(a, b, color=GREY, buff=0.12, width=5):
    return Arrow(a, b, buff=buff, color=color, stroke_width=width, tip_length=0.22)


def gene_bar(y=0.45, broken=False, label="chosen gene", width=9.8):
    """The carried purple gene bar, rebuilt at the same scale and place."""
    if not broken:
        bar = RoundedRectangle(corner_radius=0.16, width=width, height=1.05,
                               stroke_color=PURPLE, stroke_width=4,
                               fill_color=PURPLE, fill_opacity=0.22).move_to([0, y, 0])
        text = T(label, 32, TEXT, weight=BOLD)
        plate = RoundedRectangle(corner_radius=0.08, width=text.width + 0.32, height=text.height + 0.18,
                                 stroke_width=0, fill_color=BG, fill_opacity=0.92).move_to(bar)
        lab = VGroup(plate, text.move_to(plate))
        return VGroup(bar, lab)
    left = RoundedRectangle(corner_radius=0.12, width=4.45, height=1.05,
                            stroke_color=PURPLE, stroke_width=4,
                            fill_color=PURPLE, fill_opacity=0.22).move_to([-2.55, y, 0])
    right = left.copy().move_to([2.55, y, 0])
    return VGroup(left, right)


def target_blocks(y=2.2):
    guide = boxed_label("guide", BLUE, size=30, box=(2.15, 0.72)).move_to([-2.0, y, 0])
    cas9 = boxed_label("Cas9", GOLD, size=30, box=(2.15, 0.72)).move_to([0.6, y, 0])
    return guide, cas9


def function_gauge(center=(4.7, -0.8, 0), value=0.52, label="function?"):
    tracker = ValueTracker(value)
    gauge = dial(tracker, center=center, radius=1.05, label=label, color=GREEN, fmt="?", scale=0, size=44)
    return gauge, tracker


def allele_card(text, color=PURPLE, width=2.25, height=0.72, size=26):
    return boxed_label(text, color, size=size, box=(width, height), fill_opacity=0.20)


def culture_dish(with_slots=True):
    """The carried culture dish used by the predict beat and its pause."""
    dish = Ellipse(width=9.2, height=4.25, stroke_color=GREY, stroke_width=4,
                   fill_color=GREY, fill_opacity=0.07).move_to([0, -0.25, 0])
    cells = VGroup()
    for x, y in [(-2.8, 0.25), (-0.95, -0.7), (0.95, 0.35), (2.8, -0.65)]:
        c = Circle(radius=0.72, stroke_color=GREY, stroke_width=3,
                   fill_color=GREY, fill_opacity=0.13).move_to([x, y, 0])
        if with_slots:
            slots = VGroup(*[RoundedRectangle(corner_radius=0.06, width=0.68, height=0.22,
                                               stroke_color=PURPLE, stroke_width=2,
                                               fill_color=PURPLE, fill_opacity=0.18)
                             for _ in range(2)]).arrange(DOWN, buff=0.16).move_to(c)
            cells.add(VGroup(c, slots))
        else:
            cells.add(c)
    return VGroup(dish, cells)


def predict_world():
    dish = culture_dish()
    cards = VGroup(allele_card("unchanged", GREY, width=2.45),
                   allele_card("shortened", PURPLE, width=2.45),
                   allele_card("lengthened", PURPLE, width=2.45))
    cards.arrange(RIGHT, buff=0.38).move_to([0, 2.45, 0])
    return VGroup(dish, cards)


def checkpoint_pipeline():
    """The carried four-checkpoint picture for s04 and s11."""
    xs = [-4.7, -1.6, 1.6, 4.7]
    target = VGroup(boxed_label("guide", BLUE, 26, box=(1.65, 0.62)),
                    boxed_label("Cas9", GOLD, 26, box=(1.65, 0.62))).arrange(DOWN, buff=0.18).move_to([xs[0], 0.45, 0])
    cut = gene_bar(y=0.45, broken=True, width=3.0).scale(0.46).move_to([xs[1], 0.45, 0])
    edited = allele_card("changed", PURPLE, width=2.05, height=0.82).move_to([xs[2], 0.45, 0])
    ftrack = ValueTracker(0.52)
    func = dial(ftrack, [xs[3], 0.75, 0], radius=0.82, label="function?", color=GREEN, fmt="?", scale=0, size=38)
    pics = VGroup(target, cut, edited, func)
    labels = VGroup(T("targeted site", 28, BLUE), T("cut", 28, PURPLE),
                    T("edited allele", 28, PURPLE), T("functional\nknockout?", 28, GREEN))
    for x, lab in zip(xs, labels):
        lab.move_to([x, -1.35, 0])
    arrows = VGroup(*[arrow_between([xs[i] + 1.0, 0.45, 0], [xs[i + 1] - 1.0, 0.45, 0]) for i in range(3)])
    field = RoundedRectangle(corner_radius=0.2, width=12.5, height=3.55,
                             stroke_color=GREY, stroke_width=0,
                             fill_color=GREY, fill_opacity=0.10).move_to([0, 0.15, 0])
    g = VGroup(field, pics, labels, arrows)
    g.pics = pics
    g.labels = labels
    g.arrows = arrows
    g.ftrack = ftrack
    return g


def tiny_meter(at, label="?"):
    box = RoundedRectangle(corner_radius=0.1, width=1.12, height=0.46,
                           stroke_color=GREEN, stroke_width=2.5,
                           fill_color=GREEN, fill_opacity=0.12).move_to(at)
    return VGroup(box, T(label, 28, GREEN).move_to(box))


def bar_meter(center, tracker, label="phenotype", width=1.75):
    """A compact live readout whose fill is tied to the same tracker as its claim."""
    c = np.array(center, dtype=float)
    outline = RoundedRectangle(corner_radius=0.1, width=width, height=0.62,
                               stroke_color=GREEN, stroke_width=3,
                               fill_color=BG, fill_opacity=0.9).move_to(c)
    fill = always_redraw(lambda: Rectangle(width=max(0.04, (width - 0.16) * tracker.get_value()),
                                            height=0.46, stroke_width=0,
                                            fill_color=GREEN, fill_opacity=0.65).move_to(
                                                [c[0] - (width - 0.16) / 2 + max(0.04, (width - 0.16) * tracker.get_value()) / 2,
                                                 c[1], 0]))
    lab = T(label, 24, GREEN).next_to(outline, UP, buff=0.12)
    return VGroup(outline, fill, lab)


class S00LinkAndQuestion(SpokenScene):
    LESSON = "CRISPR and functional genomics"
    TITLE = "From a Programmed Cut to a Tested Knockout"

    def construct(self):
        bench = Line([-6.1, -2.35, 0], [6.1, -2.35, 0], color=GREY, stroke_width=5)
        card = allele_card("chosen gene", PURPLE, width=2.8, height=1.0, size=30).move_to([-3.8, 0.45, 0])
        pulse(bench, base=5, amp=1.5, speed=1.8)
        bob(card, amp=0.07, speed=1.35)
        self.play(Create(bench), FadeIn(card, shift=UP * 0.2), run_time=0.8)
        self.at("what you choose first")
        bar = gene_bar(y=0.45)
        self.play(ReplacementTransform(card, bar), run_time=1.0)
        guide, cas9 = target_blocks()
        self.at("If Cas9 cuts")
        self.play(FadeIn(guide, shift=DOWN * 0.2), FadeIn(cas9, shift=DOWN * 0.2), run_time=0.8)
        self.play(guide.animate.move_to([-1.35, 1.55, 0]), cas9.animate.move_to([1.35, 1.55, 0]), run_time=1.2)
        self.at("have you made")
        gauge, tracker = function_gauge()
        path = arrow_between([2.3, 0.35, 0], [3.55, -0.35, 0], GREEN)
        self.play(GrowArrow(path), FadeIn(gauge), run_time=0.9)
        self.add(scope_tag("schematic"))
        bob(VGroup(guide, cas9), amp=0.05, speed=1.5)
        self.finish()


class S01Title(TitleCard):
    LESSON = "CRISPR and functional genomics"
    TITLE = "From a Programmed Cut to a Tested Knockout"


class S02Target(SpokenScene):
    def construct(self):
        bar = gene_bar(y=-0.15)
        guide, cas9 = target_blocks(y=2.15)
        pulse(bar[0], base=4, amp=1.5, speed=1.8)
        self.play(FadeIn(bar), FadeIn(guide), FadeIn(cas9), run_time=0.8)
        self.play(guide.animate.move_to([-1.35, 1.25, 0]), cas9.animate.move_to([1.35, 1.25, 0]), run_time=1.3)
        match = T("matching region", 28, PURPLE).move_to([0, -1.05, 0])
        self.at("matching purple gene")
        self.play(FadeIn(match), run_time=0.5)
        pam = boxed_label("PAM", ORANGE, 30, box=(1.45, 0.7)).move_to([3.55, 0.75, 0])
        self.at("nearby orange")
        self.play(FadeIn(pam, scale=0.8), run_time=0.6)
        pulse(pam[0], base=3.0, amp=1.6, speed=3.0)
        no_pam = VGroup(RoundedRectangle(corner_radius=0.12, width=3.05, height=0.75,
                                         stroke_color=GREY, stroke_width=3, fill_opacity=0),
                        T("matching site   ?", 26, GREY)).move_to([-4.1, -2.05, 0])
        self.at("Without a PAM")
        self.play(FadeIn(no_pam), bar.animate.set_opacity(0.72), run_time=0.7)
        self.at("With it")
        self.play(FadeOut(no_pam), bar.animate.set_opacity(1), run_time=0.5)
        broken = gene_bar(y=-0.15, broken=True)
        self.play(FadeOut(bar[1]), ReplacementTransform(bar[0], broken), FadeOut(match), run_time=0.9)
        ends = VGroup(T("broken end", 26, PURPLE).move_to([-1.0, -1.1, 0]),
                      T("broken end", 26, PURPLE).move_to([1.0, -1.1, 0]))
        self.play(FadeIn(ends), run_time=0.5)
        bob(VGroup(guide, cas9), amp=0.035, speed=1.6)
        self.finish()


class S03Repair(SpokenScene):
    def construct(self):
        broken = gene_bar(y=2.15, broken=True)
        pulse(broken[0], base=4, amp=1.4, speed=1.7)
        pulse(broken[1], base=4, amp=1.4, speed=1.7)
        self.play(FadeIn(broken), run_time=0.6)
        fork = VGroup(arrow_between([-0.35, 1.6, 0], [-3.0, 0.7, 0], GREY),
                      arrow_between([0.35, 1.6, 0], [3.0, 0.7, 0], GREY))
        self.at("only a handoff")
        self.play(*[GrowArrow(a) for a in fork], run_time=0.8)
        upper = VGroup(allele_card("restored", PURPLE, width=2.15),
                       allele_card("insertion", PURPLE, width=2.15),
                       allele_card("deletion", PURPLE, width=2.15)).arrange(DOWN, buff=0.28).move_to([-3.55, -0.6, 0])
        self.at("rejoins ends")
        self.play(FadeIn(upper[0]), run_time=0.6)
        self.at("restore the sequence")
        self.play(FadeIn(upper[1], shift=DOWN * 0.15), FadeIn(upper[2], shift=UP * 0.15), run_time=0.9)
        template = boxed_label("supplied template", GREY, 28, box=(3.4, 0.72)).move_to([3.5, -1.5, 0])
        repaired = allele_card("template-copied allele", PURPLE, width=3.7).move_to([3.5, -0.15, 0])
        self.at("Another root copies")
        self.play(FadeIn(template), run_time=0.5)
        self.play(GrowFromEdge(repaired, LEFT), run_time=0.9)
        self.at("several repaired alleles")
        fan = VGroup(*[c.copy() for c in upper], repaired.copy()).arrange(RIGHT, buff=0.24).move_to([0, -2.25, 0])
        self.play(ReplacementTransform(VGroup(upper, repaired), fan), FadeOut(template), run_time=1.0)
        tag = T("possible outcomes", 28, GREY).move_to([0, -3.05, 0])
        self.play(FadeIn(tag), run_time=0.4)
        self.add(scope_tag("schematic"))
        bob(fan, amp=0.035, speed=1.4)
        self.finish()


class S04Checkpoints(SpokenScene):
    def construct(self):
        pipe = checkpoint_pipeline()
        bob(pipe.pics, amp=0.075, speed=1.25)
        self.play(FadeIn(pipe.pics), run_time=0.7)
        self.at("through each checkpoint")
        self.play(*[GrowArrow(a) for a in pipe.arrows], run_time=0.8)
        cues = ["Targeting means", "A cut means", "An edited allele", "A functional knockout"]
        badges = VGroup()
        for i, cue in enumerate(cues):
            self.at(cue)
            self.play(FadeIn(pipe.labels[i], shift=UP * 0.12), run_time=0.45)
            if i < 3:
                badge = boxed_label("evidence", GREY, 24, box=(1.45, 0.55)).move_to([pipe.labels[i].get_x(), -2.25, 0])
                badges.add(badge)
                self.play(FadeIn(badge), run_time=0.35)
        self.at("different evidence")
        self.play(Indicate(pipe.labels[3], color=GREEN, scale_factor=1.04), run_time=0.7)
        pulse(pipe.pics[3][0], base=10, amp=2, speed=2)
        self.finish()


class S05Predict(SpokenScene):
    def construct(self):
        world = predict_world()
        dish, cards = world
        bob(dish, amp=0.06, speed=1.25)
        bob(cards, amp=0.055, speed=1.4)
        self.play(FadeIn(dish), run_time=0.8)
        self.at("several repaired")
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in cards], lag_ratio=0.2), run_time=1.0)
        self.at("Some are unchanged")
        self.play(cards.animate.shift(RIGHT * 0.18), run_time=0.45)
        self.play(cards.animate.shift(LEFT * 0.36), run_time=0.45)
        self.play(cards.animate.shift(RIGHT * 0.18), run_time=0.45)
        self.at("Must every cell")
        q = question_card("Did every cell lose function?", color=GOLD, size=34)
        self.play(FadeIn(q.question, shift=UP * 0.12), run_time=0.7)
        for cell in dish[1]:
            pulse(cell[1], base=2.0, amp=0.7, speed=2.0)
        self.finish()


class S06PredictPause(PredictPause):
    QUESTION = "Did every cell lose function?"
    SECONDS = 4.5

    def backdrop(self):
        world = predict_world()
        bob(world[1], amp=0.045, speed=1.3)
        for cell in world[0][1]:
            pulse(cell[1], base=2.0, amp=0.7, speed=2.0)
        return world


class S07MixedCells(SpokenScene):
    def construct(self):
        dish = culture_dish(with_slots=False)
        dish[1].set_stroke(opacity=0)
        bob(dish, amp=0.055, speed=1.25)
        xys = [(-3.0, 0.25), (-1.05, -0.7), (1.25, 0.35), (3.3, -0.65)]
        for cell, (x, y) in zip(dish[1], xys):
            cell.move_to([x, y, 0])
        self.play(FadeIn(dish), run_time=0.6)
        heading = T("mixed population", 36, GREY, weight=BOLD).move_to([0, 3.15, 0])
        self.at("cells can carry")
        self.play(FadeIn(heading), run_time=0.5)
        pairs = [("unchanged", "shortened"), ("in-frame", "shortened"),
                 ("frameshift", "frameshift"), ("changed A", "changed B")]
        card_groups, meters = VGroup(), VGroup()
        for (a, b), (x, y) in zip(pairs, xys):
            cg = VGroup(allele_card(a, GREY if a == "unchanged" else PURPLE, 1.65, 0.56, 22),
                        allele_card(b, PURPLE, 1.65, 0.56, 22)).arrange(DOWN, buff=0.35).move_to([x, y, 0])
            card_groups.add(cg)
            meters.add(tiny_meter([x, y - 1.28, 0]))
        bob(card_groups, amp=0.2, speed=1.4)
        self.at("diploid cell carries")
        self.play(FadeOut(dish[0]),
                  LaggedStart(*[FadeIn(cg, scale=0.9) for cg in card_groups], lag_ratio=0.18), run_time=1.4)
        self.at("unchanged or in")
        self.play(Indicate(card_groups[0], color=GREY), Indicate(card_groups[1], color=PURPLE), run_time=0.8)
        self.at("frameshifts in both")
        self.play(Indicate(card_groups[2], color=PURPLE), run_time=0.7)
        self.play(FadeIn(meters), run_time=0.5)
        self.at("allele count is not")
        counts = VGroup(boxed_label("alleles", PURPLE, 28, box=(2.0, 0.7)),
                        boxed_label("cells", GREY, 28, box=(2.0, 0.7))).arrange(RIGHT, buff=1.1).move_to([0, -3.0, 0])
        neq = T("≠", 42, TEXT).move_to([0, -3.0, 0])
        self.play(FadeIn(counts), FadeIn(neq), run_time=0.7)
        for m in meters:
            self.play(Indicate(m, color=GREEN, scale_factor=1.25), run_time=1.0)
        self.finish()


class S08Function(SpokenScene):
    def construct(self):
        tp = TwoPanel("sequence prediction", "functional measurement", colors=(PURPLE, GREEN), top=3.0, bottom=-2.45)
        tp.left_frame.set_fill(PURPLE, opacity=0.08)
        tp.right_frame.set_fill(GREEN, opacity=0.08)
        pulse(tp.left_frame, base=2.5, amp=0.8, speed=1.4)
        pulse(tp.right_frame, base=2.5, amp=0.8, speed=1.6)
        self.play(FadeIn(tp), run_time=0.7)
        fs = VGroup(allele_card("frameshift", PURPLE, width=2.55),
                    allele_card("frameshift", PURPLE, width=2.55)).arrange(DOWN, buff=0.25)
        tp.put(fs, "left")
        self.play(FadeIn(fs), run_time=0.6)
        self.at("sequence predictions")
        shifted = VGroup(*[Square(0.28, stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=0.35) for _ in range(10)]).arrange(RIGHT, buff=0.09)
        shifted[4:].shift(RIGHT * 0.18)
        shifted.move_to([-3.2, -1.4, 0])
        self.play(LaggedStart(*[FadeIn(s) for s in shifted], lag_ratio=0.08), run_time=0.9)
        protein = boxed_label("protein output   ?", GREY, 30, box=(3.35, 0.9)).move_to([3.25, 0.9, 0])
        dotted = DashedLine([-1.4, 0.45, 0], protein.get_left() + LEFT * 0.12, color=GREY, stroke_width=4)
        self.at("Whether the protein's")
        self.play(Create(dotted), FadeIn(protein), run_time=0.8)
        partial = allele_card("in-frame", PURPLE, width=2.0).move_to([2.35, -0.45, 0])
        meter = boxed_label("possible partial function", GREEN, 26, box=(3.3, 0.78)).move_to([3.65, -1.55, 0])
        self.at("in frame change")
        self.play(FadeIn(partial), run_time=0.5)
        self.play(FadeIn(meter), run_time=0.6)
        unexpected = boxed_label("unexpected product?", GREY, 26, box=(3.0, 0.7)).move_to([3.5, -2.15, 0])
        self.at("Genotype narrows")
        self.play(swap(meter, unexpected), run_time=0.7)
        self.add(scope_tag("schematic possibilities"))
        pulse(protein[0], base=2.5, amp=0.8, speed=2.0)
        self.finish()


class S09Measure(SpokenScene):
    def construct(self):
        steps = ["clone", "genotype", "product", "phenotype"]
        colors = [GREY, PURPLE, GREY, GREEN]
        xs = [-4.8, -1.6, 1.6, 4.8]
        nodes = VGroup(*[boxed_label(s, c, 28, box=(2.05, 0.78)).move_to([x, -2.1, 0])
                         for s, c, x in zip(steps, colors, xs)])
        arrows = VGroup(*[arrow_between(nodes[i].get_right(), nodes[i + 1].get_left()) for i in range(3)])
        step_field = Rectangle(width=12.5, height=1.28, stroke_width=0,
                               fill_color=GREY, fill_opacity=0.10).move_to([0, -2.1, 0])
        cell = Circle(radius=0.62, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.13).move_to([-4.8, 0.7, 0])
        clones = VGroup(*[cell.copy().scale(0.62) for _ in range(6)]).arrange_in_grid(2, 3, buff=0.22).move_to([-4.8, 0.7, 0])
        bob(clones, amp=0.075, speed=1.25)
        self.play(FadeIn(step_field), FadeIn(cell), FadeIn(nodes[0]), run_time=0.6)
        self.at("single cell clones")
        self.play(ReplacementTransform(cell, clones), run_time=0.9)
        alleles = VGroup(allele_card("allele 1", PURPLE, width=2.2), allele_card("allele 2", PURPLE, width=2.2)).arrange(DOWN, buff=0.3).move_to([-1.6, 0.7, 0])
        self.play(GrowArrow(arrows[0]), FadeIn(nodes[1]), FadeIn(alleles), run_time=0.8)
        window = Rectangle(width=0.8, height=1.9, stroke_color=GOLD, stroke_width=4).move_to([-2.1, 0.7, 0])
        self.at("short amplicon")
        self.play(FadeOut(alleles[0][1]), FadeOut(alleles[1][1]), Create(window),
                  window.animate.shift(RIGHT * 0.5), run_time=0.9)
        self.at("large changes")
        long_window = Rectangle(width=2.45, height=1.9, stroke_color=GOLD, stroke_width=4).move_to([-1.6, 0.7, 0])
        self.play(ReplacementTransform(window, long_window), run_time=0.7)
        prod = boxed_label("gene product / activity", GREY, 28, box=(2.85, 1.0)).move_to([2.05, 0.7, 0])
        self.at("Measure the gene product")
        self.play(GrowArrow(arrows[1]), FadeIn(nodes[2]), FadeIn(prod), run_time=0.8)
        pval = ValueTracker(0.25)
        phen = dial(pval, [4.8, 1.0, 0], radius=1.0, label="phenotype", color=GREEN, fmt="{:0.0f}%", scale=100, size=34)
        self.at("phenotype follows")
        self.play(GrowArrow(arrows[2]), FadeIn(nodes[3]), FadeIn(phen), run_time=0.8)
        self.play(pval.animate.set_value(0.72), run_time=1.0)
        self.at("claim forward")
        self.play(Indicate(nodes, color=GOLD, scale_factor=1.02), run_time=0.8)
        self.finish()


class S10Controls(SpokenScene):
    def construct(self):
        tp = TwoPanel("independent guides", "resistant restoration", colors=(BLUE, PURPLE), top=3.0, bottom=-2.5)
        tp.left_frame.set_fill(BLUE, opacity=0.08)
        tp.right_frame.set_fill(PURPLE, opacity=0.08)
        pulse(tp.left_frame, base=2.5, amp=0.8, speed=1.4)
        pulse(tp.right_frame, base=2.5, amp=0.8, speed=1.6)
        self.play(FadeIn(tp), run_time=0.6)
        bars = VGroup(*[RoundedRectangle(corner_radius=0.1, width=3.2, height=0.58,
                                         stroke_color=PURPLE, stroke_width=3,
                                         fill_color=PURPLE, fill_opacity=0.22) for _ in range(2)])
        bars.arrange(DOWN, buff=1.15).move_to([-3.05, 0.35, 0])
        guides = VGroup(boxed_label("guide A", BLUE, 24, box=(1.3, 0.62)),
                        boxed_label("guide B", BLUE, 24, box=(1.3, 0.62))).arrange(DOWN, buff=1.15).move_to([-5.55, 0.35, 0])
        self.at("independent guides")
        self.play(FadeIn(bars), FadeIn(guides, shift=RIGHT * 0.2), run_time=0.9)
        gt1, gt2 = ValueTracker(0.75), ValueTracker(0.75)
        gm1 = bar_meter([-1.15, 1.22, 0], gt1, width=1.2)
        gm2 = bar_meter([-1.15, -0.52, 0], gt2, width=1.2)
        self.at("reproduce the phenotype")
        self.play(FadeIn(gm1), FadeIn(gm2), run_time=0.7)
        self.play(gt1.animate.set_value(0.25), gt2.animate.set_value(0.25), run_time=1.0)
        tag = boxed_label("guide-specific?", GREY, 24, box=(2.65, 0.72)).move_to([-3.2, -2.05, 0])
        self.at("guide specific effect")
        self.play(FadeIn(tag), run_time=0.5)
        small_tag = boxed_label("guide-specific?", GREY, 22, box=(2.3, 0.64)).move_to(tag)
        self.play(swap(tag, small_tag), run_time=0.6)
        resistant = allele_card("resistant gene", PURPLE, width=2.8, height=0.85).move_to([3.2, 1.35, 0])
        self.at("Restore the gene")
        self.play(FadeIn(resistant, shift=DOWN * 0.2), run_time=0.7)
        rv = ValueTracker(0.22)
        rescue = bar_meter([3.2, -0.2, 0], rv, width=2.3)
        self.play(FadeIn(rescue), run_time=0.5)
        self.at("phenotype reverses")
        self.play(rv.animate.set_value(0.78), run_time=1.1)
        support = boxed_label("stronger support", GREEN, 28, box=(2.8, 0.75)).move_to([3.2, -1.75, 0])
        self.play(FadeIn(support), run_time=0.6)
        self.at("no single control")
        self.play(Indicate(support, color=GREY, scale_factor=1.03), run_time=0.7)
        self.finish()


class S11Land(SpokenScene):
    def construct(self):
        pipe = checkpoint_pipeline()
        bob(pipe.pics, amp=0.075, speed=1.25)
        self.play(FadeIn(pipe), run_time=0.9)
        self.at("Cas9 can program")
        self.play(Indicate(pipe.pics[0], color=GOLD, scale_factor=1.04), run_time=0.6)
        self.at("repair determines")
        self.play(Indicate(pipe.pics[1], color=PURPLE, scale_factor=1.05), run_time=0.6)
        self.at("Sequencing can identify")
        self.play(Indicate(pipe.pics[2], color=PURPLE, scale_factor=1.05), run_time=0.6)
        readouts = VGroup(boxed_label("phenotype", GREEN, 25, box=(1.7, 0.58)),
                          boxed_label("molecular readout", GREY, 24, box=(2.45, 0.58))).arrange(DOWN, buff=0.18).move_to([4.7, -2.55, 0])
        self.at("function needs")
        self.play(FadeIn(readouts), run_time=0.7)
        badges = VGroup(*[boxed_label("evidence", GREY, 24, box=(1.45, 0.55)).move_to([x, 2.3, 0])
                          for x in [-4.7, -1.6, 1.6]])
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in badges], lag_ratio=0.18), run_time=0.9)
        self.play(FadeOut(badges), run_time=0.4)
        bracket = Brace(VGroup(pipe.pics[2], pipe.pics[3], readouts), UP, color=GOLD)
        agree = T("agreement across tests", 28, GOLD).next_to(bracket, UP, buff=0.12)
        self.at("agree across independent")
        self.play(GrowFromCenter(bracket), FadeIn(agree), run_time=0.8)
        claim = boxed_label("supported claim", GREEN, 30, box=(2.85, 0.8)).move_to([0, -3.0, 0])
        self.at("claim earns support")
        self.play(FadeIn(claim, shift=UP * 0.15), run_time=0.7)
        pulse(claim[0], base=2.5, amp=0.8, speed=2.0)
        self.finish()


class S12End(EndCard):
    LINE = "A genetic change supports function only when genotype and phenotype agree."
