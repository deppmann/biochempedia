"""Rebuilding the Memory (Biochemistrypedia explainer, eukaryotic regulation chapter 2).

COLOR MAP (one colour per concept, whole film)
  BLUE     = DNA
  GOLD     = nucleosomes
  WHITE    = promoter / gene-copy slots
  TEAL     = enhancer
  GREEN    = regulators and maintenance machinery
  MAGENTA  = DNA-methylation tags
  PALE_RNA = RNA
  GREY     = neutral labels, boundaries and qualifiers

The carried pictures live in builder functions below. Scenes rebuild those pictures at identical
coordinates so replication, restoration and cell division remain one continuous visual world.
"""
from bp_parts import *  # noqa: F401,F403

MAGENTA = "#E58BB0"
PALE_RNA = "#D8DEE9"
DNA_Y = -0.55
TAG_XS = (-2.4, -1.25, -0.1)


def rounded_arrow(a, b, color=GREY, width=4, tip=0.18):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=width, tip_length=tip,
                 max_tip_length_to_length_ratio=0.35)


def breathe_fill(mob, base=0.14, amp=0.045, speed=0.8, seed=0):
    """Slow whole-field breathing: visible motion during long spoken holds."""
    mob._breath_t = seed * 0.7

    def update(m, dt):
        m._breath_t += dt
        m.set_fill(opacity=base + amp * np.sin(speed * m._breath_t))
    return mob.add_updater(update)


def methyl_tag(x, y, direction=UP, scale=1.0):
    """A schematic methylation tag: a magenta tab, never a molecular drawing."""
    stem = Line([x, y, 0], [x, y + 0.28 * direction[1] * scale, 0], color=MAGENTA,
                stroke_width=5 * scale)
    tab = RoundedRectangle(corner_radius=0.05, width=0.28 * scale, height=0.22 * scale,
                           stroke_color=MAGENTA, stroke_width=2.5 * scale,
                           fill_color=MAGENTA, fill_opacity=0.85).move_to(
                               [x, y + 0.39 * direction[1] * scale, 0])
    return VGroup(stem, tab)


def gene_world(tags=True, low_rna=True, division=0.0, compact=False):
    """The chapter's carried nucleus and gene, always at the same scale and position."""
    nucleus = Ellipse(width=12.1, height=5.7, stroke_color=GREY, stroke_width=3,
                      fill_color=BLUE, fill_opacity=0.14).move_to([0, 0.05, 0])
    breathe_fill(nucleus, base=0.14, amp=0.05, speed=0.75)
    # The ribbon stops at each labelled block so no stroke runs through readable text.
    dna = VGroup(*[Line([a, DNA_Y, 0], [b, DNA_Y, 0], color=BLUE, stroke_width=10)
                   for a, b in ((-5.45, -5.15), (-3.35, -1.3), (0.8, 0.95), (3.35, 5.45))])
    pulse(dna, base=16, amp=3.5, speed=1.25)
    promoter = RoundedRectangle(corner_radius=0.08, width=1.9, height=0.78,
                                stroke_color=WHITE, stroke_width=3,
                                fill_color=WHITE, fill_opacity=0.12).move_to([-0.25, DNA_Y, 0])
    promoter_label = T("promoter", 28, WHITE).move_to(promoter)
    enhancer = RoundedRectangle(corner_radius=0.08, width=1.8, height=0.72,
                                stroke_color=TEAL, stroke_width=3,
                                fill_color=TEAL, fill_opacity=0.16).move_to([-4.25, DNA_Y, 0])
    enhancer_label = T("enhancer", 26, TEAL).move_to(enhancer)
    gene = RoundedRectangle(corner_radius=0.08, width=2.4, height=0.72,
                            stroke_color=WHITE, stroke_width=3,
                            fill_color=WHITE, fill_opacity=0.1).move_to([2.15, DNA_Y, 0])
    gene_label = T("gene", 28, WHITE).move_to(gene)
    nucleosomes = VGroup(*[
        Circle(radius=0.25, color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.25)
        .move_to([x, DNA_Y + (0.16 if i % 2 else -0.16), 0])
        for i, x in enumerate((-3.0, -2.2, 3.7, 4.6))
    ])
    regulators = VGroup(*[
        RoundedRectangle(corner_radius=0.12, width=0.7, height=0.48, stroke_color=GREEN,
                         stroke_width=3, fill_color=GREEN, fill_opacity=0.22)
        .move_to([x, DNA_Y + 0.9, 0]) for x in (-4.55, -3.85)
    ])
    tag_group = VGroup(*[methyl_tag(x, DNA_Y + 0.36, UP, 0.9) for x in TAG_XS]) if tags else VGroup()
    n_rna = 2 if low_rna else 5
    rna = VGroup(*[
        CubicBezier([3.55, 0.5 + i * 0.32, 0], [4.0, 0.72 + i * 0.32, 0],
                    [4.5, 0.25 + i * 0.32, 0], [5.05, 0.5 + i * 0.32, 0],
                    color=PALE_RNA, stroke_width=4).set_opacity(0.75)
        for i in range(n_rna)
    ])
    for i, n in enumerate(nucleosomes):
        bob(n, amp=0.09, speed=1.15, seed=i)
    bob(regulators, amp=0.07, speed=1.0, seed=2)
    bob(rna, amp=0.08, speed=1.1, seed=4)
    division_line = DashedLine([0, -2.65, 0], [0, -2.65 + 5.25 * division, 0],
                               color=GREY, stroke_width=4, dash_length=0.18)
    g = VGroup(nucleus, dna, nucleosomes, enhancer, enhancer_label, promoter, promoter_label,
               gene, gene_label, regulators, tag_group, rna, division_line)
    g.nucleus, g.dna, g.nucleosomes, g.tags, g.rna = nucleus, dna, nucleosomes, tag_group, rna
    g.promoter, g.gene, g.regulators, g.division = promoter, gene, regulators, division_line
    if compact:
        g.scale(0.72).move_to([0, -0.15, 0])
    return g


def strand_pair(center=(0, 0), width=5.0, show_new=True, restored=False, labels=True):
    """One daughter duplex with aligned schematic CpG positions and old/new identity."""
    cx, cy = center
    x0, x1 = cx - width / 2, cx + width / 2
    old_y, new_y = cy + 0.76, cy - 0.76
    old = Line([x0, old_y, 0], [x1, old_y, 0], color=BLUE, stroke_width=20)
    new = Line([x0, new_y, 0], [x1 if show_new else x0, new_y, 0], color=BLUE,
               stroke_width=20)
    pulse(old, base=20, amp=5, speed=1.2)
    pulse(new, base=20, amp=5, speed=1.2)
    positions = [cx - width * 0.28, cx, cx + width * 0.28]
    old_tags = VGroup(*[methyl_tag(x, old_y + 0.03, UP, 0.82) for x in positions])
    new_tags = VGroup(*[methyl_tag(x, new_y - 0.03, DOWN, 0.82) for x in positions]) if restored else VGroup()
    ticks = VGroup(*[
        DashedLine([x, old_y - 0.25, 0], [x, new_y + 0.25, 0], color=GREY, stroke_width=2,
                   dash_length=0.08).set_opacity(0.65) for x in positions
    ])
    g = VGroup(old, new, ticks, old_tags, new_tags)
    if labels:
        old_l = T("old", 28, MAGENTA).next_to(old, LEFT, buff=0.22)
        new_l = T("new", 28, BLUE).next_to(new, LEFT, buff=0.22)
        g.add(old_l, new_l)
        g.old_label, g.new_label = old_l, new_l
    g.old, g.new, g.old_tags, g.new_tags, g.positions = old, new, old_tags, new_tags, positions
    panel = RoundedRectangle(corner_radius=0.22, width=width + 0.55, height=3.35,
                             stroke_color=GREY, stroke_width=0,
                             fill_color=BLUE, fill_opacity=0.14).move_to([cx, cy, 0]).set_z_index(-2)
    breathe_fill(panel, base=0.14, amp=0.05, speed=0.82, seed=int(abs(cx)))
    g.add(panel)
    g.panel = panel
    return g


def two_duplexes(restored=False, labels=True):
    left = strand_pair((-3.25, 0.15), width=4.35, restored=restored, labels=labels)
    right = strand_pair((3.25, 0.15), width=4.35, restored=restored, labels=labels)
    return VGroup(left, right)


def dnmt_block(at):
    return boxed_label("DNMT1", GREEN, size=30, box=(1.45, 0.68), fill_opacity=0.3).move_to(at)


def daughter_cell(center, rna_level=2, tags=True):
    cx, cy = center
    cell = Ellipse(width=5.3, height=3.6, stroke_color=GREY, stroke_width=3,
                   fill_color=BLUE, fill_opacity=0.14).move_to([cx, cy, 0])
    breathe_fill(cell, base=0.14, amp=0.05, speed=0.78, seed=int(abs(cx)))
    dna = Line([cx - 1.75, cy, 0], [cx + 1.6, cy, 0], color=BLUE, stroke_width=16)
    pulse(dna, base=16, amp=4, speed=1.3)
    promoter = RoundedRectangle(corner_radius=0.06, width=0.8, height=0.5, stroke_color=WHITE,
                                stroke_width=2.5, fill_color=WHITE, fill_opacity=0.12).move_to([cx - 0.25, cy, 0])
    ts = VGroup(*[methyl_tag(cx - 0.8 + i * 0.52, cy + 0.27, UP, 0.65) for i in range(3)]) if tags else VGroup()
    rna = VGroup(*[Line([cx + 1.0, cy + 0.55 + i * 0.25, 0],
                            [cx + 1.75, cy + 0.55 + i * 0.25, 0], color=PALE_RNA, stroke_width=3)
                       for i in range(rna_level)])
    g = VGroup(cell, dna, promoter, ts, rna)
    bob(rna, amp=0.1, speed=1.1, seed=int(abs(cx)))
    g.rna, g.tags = rna, ts
    return g


def predict_backdrop():
    pairs = two_duplexes(restored=False, labels=False)
    left = boxed_label("old marked strand?", MAGENTA, size=28).move_to([-3.25, 2.25, 0])
    right = boxed_label("new unmarked strand?", BLUE, size=28).move_to([3.25, 2.25, 0])
    return VGroup(pairs, left, right)


class S00LinkHook(SpokenScene):
    def construct(self):
        world = gene_world(tags=True, low_rna=True, division=0.0)
        self.play(FadeIn(world.nucleus), Create(world.dna), run_time=0.9)
        self.play(FadeIn(VGroup(*world[2:11])), run_time=0.8)
        scope = scope_tag("schematic")
        self.add(scope)
        self.at("why do daughter cells")
        q = fit_text("Why is silence remembered?", max_w=8.6, size=40, color=TEXT).move_to([0, 3.25, 0])
        self.play(FadeIn(q, shift=DOWN * 0.12), run_time=0.6)
        self.at("access and regulators")
        self.play(Indicate(VGroup(world.nucleosomes, world.regulators), color=GREEN, scale_factor=1.05), run_time=0.9)
        self.at("through replication and division")
        self.play(Create(world.division), run_time=2.1, rate_func=linear)
        self.at("sequence survives")
        self.play(Indicate(world.dna, color=BLUE, scale_factor=1.015), run_time=0.8)
        self.at("state still needs maintenance")
        self.play(LaggedStart(*[Indicate(t, color=MAGENTA, scale_factor=1.15) for t in world.tags],
                              lag_ratio=0.2), run_time=1.4)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Eukaryotic Gene Regulation and Epigenetics"
    TITLE = "Rebuilding the Memory"


class S02Replication(SpokenScene):
    def construct(self):
        template = strand_pair((0, 0.1), width=10.2, show_new=False, labels=False)
        self.add(template.old, template.old_tags, scope_tag("schematic"))
        self.at("copies the")
        second = template.old.copy().shift(DOWN * 0.84)
        self.play(TransformFromCopy(template.old, second), run_time=1.1)
        self.at("does not automatically")
        no_auto = T("marks are not copied automatically", 32, MAGENTA).move_to([0, 2.55, 0])
        self.play(FadeIn(no_auto), run_time=0.6)
        self.at("methylated CpG site")
        legend = boxed_label("magenta tag = methylated CpG", MAGENTA, size=28).move_to([0, 2.55, 0])
        self.play(swap(no_auto, legend), run_time=0.7)
        self.play(LaggedStart(*[Indicate(t, color=MAGENTA, scale_factor=1.18) for t in template.old_tags],
                              lag_ratio=0.15), run_time=1.0)
        self.at("Each daughter duplex")
        self.play(FadeOut(VGroup(template.old, second, template.old_tags, legend)), run_time=0.5)
        pairs = two_duplexes(restored=False, labels=True)
        # Show old strands first; grow each new partner left-to-right on the next sentence.
        self.play(FadeIn(VGroup(pairs[0].old, pairs[0].old_tags, pairs[0].old_label,
                                  pairs[1].old, pairs[1].old_tags, pairs[1].old_label)), run_time=0.7)
        self.at("partner is a new")
        self.play(Create(pairs[0].new), Create(pairs[1].new), run_time=1.5, rate_func=linear)
        self.play(FadeIn(VGroup(pairs[0].new_label, pairs[1].new_label,
                                pairs[0][2], pairs[1][2])), run_time=0.5)
        self.finish()


class S03Asymmetry(SpokenScene):
    def construct(self):
        pairs = two_duplexes(restored=False, labels=True)
        self.add(pairs, scope_tag("schematic"))
        self.at("now differ")
        braces = VGroup(*[BraceBetweenPoints([x, -0.62, 0], [x, 0.92, 0], direction=RIGHT,
                                             color=GREY) for x in (-0.62, 5.42)])
        self.play(Create(braces), run_time=0.8)
        self.at("inherited positional information")
        old_lab = boxed_label("old: inherited positions", MAGENTA, 28).move_to([-3.25, 2.35, 0])
        self.play(FadeIn(old_lab), run_time=0.6)
        self.at("freshly copied sequence")
        new_lab = boxed_label("new: copied sequence", BLUE, 28).move_to([3.25, 2.35, 0])
        self.play(FadeIn(new_lab), run_time=0.6)
        self.at("must distinguish them")
        mark = T("?", 64, GOLD).move_to([0, 0.1, 0])
        self.play(FadeIn(mark, scale=0.6), run_time=0.4)
        self.play(mark.animate.move_to([-0.65, 0.1, 0]), run_time=0.65)
        self.play(mark.animate.move_to([0.65, 0.1, 0]), run_time=0.65)
        self.at("regain a similar pattern")
        self.play(mark.animate.move_to([0, 0.1, 0]), run_time=0.45)
        self.play(LaggedStart(*[Indicate(t, color=MAGENTA, scale_factor=1.14)
                                for p in pairs for t in p.old_tags], lag_ratio=0.1), run_time=1.0)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        back = predict_backdrop()
        self.add(back, scope_tag("schematic"))
        self.at("Now predict")
        q = question_card("Which strand guides restoration?", y=-2.75, size=36, max_w=10.4)
        self.play(FadeIn(q.question, shift=UP * 0.12), run_time=0.7)
        self.at("old marked strand")
        self.play(Indicate(back[1], color=MAGENTA, scale_factor=1.05), run_time=0.8)
        self.at("new unmarked strand")
        self.play(Indicate(back[2], color=BLUE, scale_factor=1.05), run_time=0.8)
        self.at("same CpG positions")
        self.play(LaggedStart(*[Indicate(p[2], color=GREY, scale_factor=1.04) for p in back[0]],
                              lag_ratio=0.2), run_time=1.0)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Which strand guides restoration?"
    SECONDS = 4.5
    CARD = {"y": -2.75, "size": 36, "max_w": 10.4}

    def backdrop(self):
        return predict_backdrop()


class S06Restore(SpokenScene):
    def construct(self):
        pairs = two_duplexes(restored=False, labels=True)
        self.add(pairs, scope_tag("schematic"))
        old_head = boxed_label("old marked strand", MAGENTA, 30).move_to([-3.25, 2.58, 0])
        new_head = boxed_label("new unmarked strand", BLUE, 30).move_to([3.25, 2.58, 0])
        self.add(old_head, new_head)
        self.at("old marked strand supplies")
        self.play(Indicate(old_head, color=MAGENTA, scale_factor=1.06), new_head.animate.set_opacity(0.25),
                  run_time=0.8)
        heading = T("maintenance methylation", 32, GREEN).move_to([0, 3.38, 0])
        self.at("Guided to these")
        self.play(FadeIn(heading), run_time=0.5)
        blocks = VGroup(dnmt_block([-5.0, 1.78, 0]), dnmt_block([1.5, 1.78, 0]))
        self.play(FadeIn(blocks, shift=DOWN * 0.15), run_time=0.5)
        self.at("copies the old pattern")
        new_tags = [methyl_tag(x, p.new.get_y() - 0.03, DOWN, 0.82) for p in pairs for x in p.positions]
        for i in range(3):
            self.play(blocks[0].animate.move_to([pairs[0].positions[i], 1.78, 0]),
                      blocks[1].animate.move_to([pairs[1].positions[i], 1.78, 0]), run_time=0.55)
            self.play(FadeIn(new_tags[i], shift=UP * 0.08),
                      FadeIn(new_tags[i + 3], shift=UP * 0.08), run_time=0.28)
        self.at("main maintenance enzyme")
        self.play(Indicate(blocks, color=GREEN, scale_factor=1.06), run_time=0.8)
        self.at("Other methyltransferases")
        other = fit_text("new patterns: other methyltransferases", max_w=6.8, size=28,
                         color=GREY).move_to([0, -2.35, 0])
        self.play(FadeIn(other, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07PromoterEffect(SpokenScene):
    def construct(self):
        world = gene_world(tags=True, low_rna=False, division=0.0)
        # Focus on the promoter while preserving its coordinates in the carried world.
        focus = RoundedRectangle(corner_radius=0.25, width=12.0, height=4.7, stroke_width=0,
                                 fill_color=BLUE, fill_opacity=0.14).move_to([0, -0.15, 0]).set_z_index(-3)
        breathe_fill(focus, base=0.14, amp=0.05, speed=0.76)
        self.add(focus, world.dna, world.promoter, world[6], world.gene, world[8],
                 world.tags, world.rna, scope_tag("schematic"))
        self.at("dense methylation")
        dense = fit_text("dense promoter CpG methylation", max_w=6.5, size=34,
                         color=MAGENTA).move_to([-1.6, 3.25, 0])
        self.play(FadeIn(dense), LaggedStart(*[Indicate(t, color=MAGENTA, scale_factor=1.18)
                                               for t in world.tags], lag_ratio=0.15), run_time=1.2)
        self.at("goes with a silent gene")
        qualifier = boxed_label("goes with silence", MAGENTA, 30).move_to([-4.35, 1.85, 0])
        self.play(FadeIn(qualifier), run_time=0.6)
        self.play(FadeOut(world.rna[2:]), run_time=0.8)
        self.at("promoter specific limits")
        limits = boxed_label("promoter-specific limits", GREY, 28).move_to([-4.45, 0.8, 0])
        self.play(FadeIn(limits), run_time=0.5)
        self.at("keep that promoter quiet")
        low = T("low RNA", 30, PALE_RNA).move_to([4.25, -1.2, 0])
        self.play(FadeIn(low), Indicate(world.promoter, color=WHITE, scale_factor=1.05), run_time=0.9)
        self.finish()


class S08CellMemory(SpokenScene):
    def construct(self):
        pairs = two_duplexes(restored=False, labels=False)
        blocks = VGroup(dnmt_block([-5.0, 1.85, 0]), dnmt_block([1.5, 1.85, 0]))
        self.add(pairs, blocks, scope_tag("schematic"))
        self.at("pattern is restored")
        added = VGroup()
        for i in range(3):
            ts = VGroup(*[methyl_tag(p.positions[i], p.new.get_y() - 0.03, DOWN, 0.82) for p in pairs])
            added.add(*ts)
            self.play(blocks[0].animate.move_to([pairs[0].positions[i], 1.85, 0]),
                      blocks[1].animate.move_to([pairs[1].positions[i], 1.85, 0]), run_time=0.42)
            self.play(FadeIn(ts), run_time=0.22)
        self.at("both daughters")
        self.play(FadeOut(VGroup(pairs, blocks, added)), run_time=0.45)
        daughters = VGroup(daughter_cell((-3.15, 0.15), rna_level=2),
                           daughter_cell((3.15, 0.15), rna_level=3))
        self.play(FadeIn(daughters, scale=0.95), run_time=0.8)
        bridge = T("helps preserve", 34, GREEN).move_to([0, 2.6, 0])
        self.play(FadeIn(bridge), run_time=0.5)
        self.at("does not guarantee")
        neq = T("not identical", 30, GOLD).move_to([0, -2.25, 0])
        self.play(FadeIn(neq), run_time=0.5)
        self.at("hard to read")
        self.play(daughters[0].rna.animate.set_opacity(0.45), daughters[1].rna.animate.set_opacity(0.62),
                  run_time=0.8)
        self.at("Similar does not")
        self.play(daughters[0].rna.animate.shift(UP * 0.12), daughters[1].rna.animate.shift(DOWN * 0.1),
                  run_time=0.5, rate_func=there_and_back)
        self.finish()


def lineage_tree():
    root = [0, 2.0, 0]
    nodes = [(0, 2.0), (-2.7, 0.4), (2.7, 0.4), (-4.2, -1.7), (-1.4, -1.7),
             (1.4, -1.7), (4.2, -1.7)]
    dots = VGroup(*[Dot([x, y, 0], radius=0.18, color=BLUE) for x, y in nodes])
    edges = VGroup(*[Line(root if i < 2 else [nodes[1 + (i-2)//2][0], nodes[1 + (i-2)//2][1], 0],
                              [nodes[i+1][0], nodes[i+1][1], 0], color=BLUE, stroke_width=5)
                     for i in range(6)])
    slots = VGroup()
    for x, y in nodes[1:]:
        bright = RoundedRectangle(corner_radius=0.05, width=0.55, height=0.32, color=WHITE,
                                  fill_color=WHITE, fill_opacity=0.12).move_to([x - 0.38, y - 0.5, 0])
        dim = bright.copy().shift(RIGHT * 0.76).set_opacity(0.28)
        slots.add(VGroup(bright, dim))
    g = VGroup(edges, dots, slots)
    pulse(edges, base=5, amp=2.5, speed=1.15)
    g.edges, g.dots, g.slots = edges, dots, slots
    return g


class S09Epigenetic(SpokenScene):
    def construct(self):
        tree = lineage_tree()
        self.play(FadeIn(tree.dots[0]), run_time=0.3)
        self.at("inherited across cell divisions")
        self.play(LaggedStart(*[Create(e) for e in tree.edges], lag_ratio=0.15),
                  LaggedStart(*[FadeIn(d) for d in tree.dots[1:]], lag_ratio=0.15), run_time=1.7)
        self.at("without changing")
        same = boxed_label("DNA sequence unchanged", BLUE, 30).move_to([0, 3.15, 0])
        self.play(FadeIn(same), run_time=0.5)
        self.at("Mitotic inheritance")
        self.play(LaggedStart(*[FadeIn(s) for s in tree.slots], lag_ratio=0.1), run_time=1.0)
        bracket = Brace(tree, DOWN, color=GREEN)
        established = T("mitotic inheritance: established", 30, GREEN).next_to(bracket, DOWN, buff=0.12)
        self.play(Create(bracket), FadeIn(established), run_time=0.7)
        self.at("X inactivation")
        self.play(FadeOut(same), run_time=0.3)
        xlab = boxed_label("X inactivation", WHITE, 30).move_to([-3.6, 2.55, 0])
        self.play(FadeIn(xlab), run_time=0.5)
        self.at("imprinting")
        ilab = boxed_label("imprinting", WHITE, 30).move_to([3.5, 2.55, 0])
        self.play(FadeIn(ilab), run_time=0.5)
        self.at("many divisions")
        self.play(LaggedStart(*[Indicate(s[1], color=WHITE, scale_factor=1.08) for s in tree.slots],
                              lag_ratio=0.1), run_time=1.1)
        self.finish()


def plant_icon(at):
    x, y = at
    stem = Line([x, y - 0.55, 0], [x, y + 0.45, 0], color=GREEN, stroke_width=6)
    leaves = VGroup(Ellipse(width=0.7, height=0.34, color=GREEN, fill_color=GREEN,
                            fill_opacity=0.3).rotate(0.45).move_to([x - 0.3, y + 0.15, 0]),
                    Ellipse(width=0.7, height=0.34, color=GREEN, fill_color=GREEN,
                            fill_opacity=0.3).rotate(-0.45).move_to([x + 0.3, y + 0.38, 0]))
    return VGroup(stem, leaves)


def worm_icon(at):
    x, y = at
    return ArcBetweenPoints([x - 0.65, y - 0.2, 0], [x + 0.65, y + 0.2, 0], angle=1.7,
                            color=GOLD, stroke_width=12)


def mammal_icon(at):
    x, y = at
    body = Ellipse(width=1.35, height=0.72, color=WHITE, fill_color=WHITE,
                   fill_opacity=0.12).move_to([x, y, 0])
    head = Circle(radius=0.3, color=WHITE, fill_color=WHITE, fill_opacity=0.12).move_to([x + 0.8, y + 0.18, 0])
    legs = VGroup(Line([x - 0.4, y - 0.28, 0], [x - 0.45, y - 0.72, 0], color=WHITE, stroke_width=5),
                  Line([x + 0.35, y - 0.28, 0], [x + 0.4, y - 0.72, 0], color=WHITE, stroke_width=5))
    return VGroup(body, head, legs)


class S10GermlineLimit(SpokenScene):
    def construct(self):
        left_tree = lineage_tree().scale(0.55).move_to([-4.0, 0.1, 0])
        left_title = T("cell divisions", 30, GREEN).move_to([-4.0, 2.45, 0])
        self.add(left_tree, left_title)
        self.at("germline is a different claim")
        divider = DashedLine([0, -2.8, 0], [0, 2.8, 0], color=GREY, stroke_width=3, dash_length=0.16)
        right_title = fit_text("germline across generations", max_w=5.5, size=32,
                               color=GOLD).move_to([3.35, 2.65, 0])
        self.play(Create(divider), FadeIn(right_title), run_time=0.8)
        plant, worm, mammal = plant_icon((1.45, 0.9)), worm_icon((3.25, 0.9)), mammal_icon((5.15, 0.9))
        bob(plant, amp=0.1, speed=1.0, seed=1)
        bob(worm, amp=0.1, speed=1.15, seed=3)
        bob(mammal, amp=0.1, speed=0.9, seed=5)
        self.at("documented in plants")
        self.play(FadeIn(plant), run_time=0.5)
        self.at("C elegans")
        self.play(FadeIn(worm), run_time=0.5)
        solid_evidence = Line([1.0, 0.0, 0], [3.75, 0.0, 0], color=GREEN, stroke_width=5)
        solid_label = T("documented", 28, GREEN).next_to(solid_evidence, DOWN, buff=0.15)
        self.play(Create(solid_evidence), FadeIn(solid_label), run_time=0.6)
        self.at("In mammals")
        self.play(FadeIn(mammal), run_time=0.5)
        path = DashedLine([4.15, -0.65, 0], [6.15, -0.65, 0], color=MAGENTA,
                          stroke_width=4, dash_length=0.16)
        tags = VGroup(*[methyl_tag(4.35 + i * 0.42, -0.68, UP, 0.55) for i in range(5)])
        self.play(Create(path), FadeIn(tags), run_time=0.7)
        self.at("erased and rewritten")
        moved = VGroup(*[methyl_tag(4.55 + i * 0.48, -0.68, UP, 0.55) for i in range(3)])
        self.play(FadeOut(tags), run_time=0.65)
        self.play(FadeIn(moved), run_time=0.65)
        reset = fit_text("most methylation erased and rewritten", max_w=5.6, size=28,
                         color=MAGENTA, max_lines=2).move_to([3.55, -1.65, 0])
        stages = T("germ cells · early embryo", 26, GREY).move_to([3.55, -2.35, 0])
        self.play(FadeIn(reset), FadeIn(stages), run_time=0.7)
        self.at("limited and contested")
        limit = boxed_label("limited and contested", GOLD, 28).move_to([0.15, -3.25, 0], aligned_edge=LEFT)
        self.play(FadeIn(limit), run_time=0.6)
        self.finish()


class S11Scope(SpokenScene):
    def construct(self):
        world = gene_world(tags=True, low_rna=True, division=0.0, compact=False)
        world.remove(world.nucleus)
        ink = VGroup(Rectangle(width=0.85, height=1.0, color=GREY, fill_color=GREY,
                               fill_opacity=0.2),
                     Polygon([-0.3, 0.5, 0], [0.3, 0.5, 0], [0.2, 0.82, 0], [-0.2, 0.82, 0],
                             color=GREY, fill_color=GREY, fill_opacity=0.2)).move_to([-4.8, 2.2, 0])
        ink_l = T("permanent ink?", 30, GREY).next_to(ink, RIGHT, buff=0.25)
        self.add(world, ink, ink_l, scope_tag("schematic"))
        self.at("not permanent ink")
        self.play(FadeOut(ink), ink_l.animate.set_color(MAGENTA), run_time=0.6)
        block = dnmt_block([-4.0, 1.0, 0])
        self.at("Maintenance machinery")
        self.play(FadeIn(block), run_time=0.5)
        self.play(block.animate.move_to([-0.8, 1.0, 0]), run_time=1.1, rate_func=linear)
        self.play(LaggedStart(*[Indicate(t, color=MAGENTA, scale_factor=1.15) for t in world.tags],
                              lag_ratio=0.15), run_time=0.8)
        self.at("other regulators can oppose")
        activator = boxed_label("activator", GREEN, 28).move_to([-0.25, 1.45, 0])
        self.play(FadeOut(block), run_time=0.25)
        self.play(FadeIn(activator), run_time=0.3)
        extra_rna = VGroup(*[
            Line([2.6, 0.45 + i * 0.24, 0], [3.65, 0.45 + i * 0.24, 0],
                 color=PALE_RNA, stroke_width=3) for i in range(3)
        ])
        self.play(FadeIn(extra_rna, shift=RIGHT * 0.15), run_time=0.8)
        self.at("active process")
        active = T("active rebuilding", 36, GREEN).move_to([0, 2.8, 0])
        self.play(FadeOut(VGroup(ink_l, activator)), FadeIn(active), run_time=0.6)
        self.at("need again each time")
        self.play(Create(world.division), run_time=1.2, rate_func=linear)
        self.at("not evidence")
        daughters = VGroup(daughter_cell((-4.9, -0.7), 2), daughter_cell((0.9, -0.7), 2)).scale(0.55)
        germ = DashedLine([2.0, -1.0, 0], [5.6, -1.0, 0], color=GOLD, stroke_width=4,
                          dash_length=0.16)
        germ_l = T("mammalian germline: limited", 28, GOLD).move_to([3.8, -1.65, 0])
        self.play(FadeOut(VGroup(world, extra_rna)), FadeIn(daughters), Create(germ), FadeIn(germ_l),
                  run_time=0.9)
        active.generate_target()
        active.target.scale(0.8).move_to([-2.0, 1.9, 0])
        self.play(MoveToTarget(active), run_time=0.5)
        self.finish()


class S12End(EndCard):
    LINE = "Cell memory requires regulatory states to be propagated or restored after replication."
