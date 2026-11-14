"""Chromosome changes, chapter 2: break, rejoin, segregate.

COLOR MAP (continued exactly from chapter 1)
  BLUE   = one homologue / its blocks
  YELLOW = the other homologue / its blocks
  TEAL   = a segment while it is moving to a new chromosome
  GREEN  = balanced dose or a balanced meiotic product
  RED    = extra or missing material / an unbalanced product
  GREY   = spindle, cells, and the nonhomologous chromosome
  TEXT   = block lettering and breakpoint highlights
"""
from bp_parts import *  # noqa: F401,F403


LETTERS = "ABCDE"
BLOCK_W, BLOCK_H, BLOCK_GAP = 1.65, 1.55, 0.10


def chromosome_blocks(letters=LETTERS, color=BLUE, center=ORIGIN, scale=1.0,
                      colors=None, vertical=False):
    """The carried chromosome picture used throughout the chapter."""
    colors = colors or [color] * len(letters)
    blocks = VGroup()
    for letter, col in zip(letters, colors):
        box = RoundedRectangle(
            corner_radius=0.12, width=BLOCK_W, height=BLOCK_H,
            stroke_color=col, stroke_width=4,
            fill_color=col, fill_opacity=0.34,
        )
        lab = T(letter, 38, TEXT, weight=BOLD).move_to(box)
        blocks.add(VGroup(box, lab))
    blocks.arrange(DOWN if vertical else RIGHT, buff=BLOCK_GAP)
    blocks.scale(scale).move_to(center)
    blocks.blocks = blocks
    return blocks


def finish_alive(scene, mob=None):
    """Use the remaining narration time for a slow, visible settling motion."""
    remaining = scene.narration_s + 0.4 - scene.elapsed()
    if remaining > 0.45:
        if mob is None:
            mob = Group(*scene.mobjects)
        cycles = max(1, int(remaining / 2.3))
        settle = lambda t: 0.5 - 0.5 * np.cos(TAU * cycles * t)
        scene.play(mob.animate.shift(UP * 0.26), run_time=remaining,
                   rate_func=settle)
    scene.finish()


def mini_chromosome(color, x, y=0, h=4.6, label=None):
    body = RoundedRectangle(
        corner_radius=0.22, width=0.62, height=h,
        stroke_color=color, stroke_width=4,
        fill_color=color, fill_opacity=0.30,
    ).move_to([x, y, 0])
    bands = VGroup(*[
        Line([x - 0.24, y + d, 0], [x + 0.24, y + d, 0], color=TEXT, stroke_width=4)
        for d in (-1.35, -0.45, 0.45, 1.35) if abs(d) < h / 2 - 0.15
    ])
    g = VGroup(body, bands)
    if label:
        g.add(T(label, 28, color).next_to(body, DOWN, buff=0.18))
    return g


def dose_meter(value=0.5, at=(4.7, 0.3, 0), color=GREEN, label="total DNA dose"):
    """Large component dial; value .5 reads 100%, lower/higher show dose loss/gain."""
    v = ValueTracker(value)
    d = dial(v, center=at, radius=1.25, label=label, color=color,
             fmt="{:.0f}%", scale=200, size=34)
    return v, d


def break_mark(x, y=0, height=1.15, color=TEXT):
    return VGroup(
        Line([x - 0.13, y + height / 2, 0], [x + 0.13, y + 0.12, 0], color=color, stroke_width=5),
        Line([x - 0.13, y - 0.12, 0], [x + 0.13, y - height / 2, 0], color=color, stroke_width=5),
    )


def question_world(with_question=True):
    """Exact final frame shared by the predict and silent-pause scenes."""
    cross = translocation_cross()
    green = VGroup(
        DashedLine([-4.2, 2.25, 0], [4.2, -2.25, 0], color=GREEN, stroke_width=5),
        DashedLine([4.2, 2.25, 0], [-4.2, -2.25, 0], color=GREEN, stroke_width=5),
    )
    red = VGroup(
        DashedLine([-4.3, 2.25, 0], [-4.3, -2.25, 0], color=RED, stroke_width=5),
        DashedLine([4.3, 2.25, 0], [4.3, -2.25, 0], color=RED, stroke_width=5),
    )
    zones = VGroup(*[
        Circle(radius=0.64, color=GREY, stroke_width=3,
               fill_color=GREY, fill_opacity=0.16).move_to(p)
        for p in ((-5.3, 2.25, 0), (5.3, 2.25, 0), (-5.3, -2.25, 0), (5.3, -2.25, 0))
    ])
    marks = VGroup(*[T("?", 34, TEXT).move_to(z) for z in zones])
    choices = VGroup(T("opposite", 27, GREEN, weight=BOLD).move_to([-4.7, 3.18, 0]),
                     T("neighbouring", 27, RED, weight=BOLD).move_to([4.55, 3.18, 0]))
    world = VGroup(cross, zones, marks, green, red, choices)
    if with_question:
        q = question_card(
            "Which pairing keeps one copy of every block?",
            [], y=-3.22, size=28, chip_size=25,
        )
        world.add(q)
    return world


def translocated_pair(scale=1.0, y=0.0):
    """Same balanced reciprocal-translocation products in every later scene."""
    blue = chromosome_blocks("ABCDg", BLUE, [-3.0, y, 0], 0.62 * scale,
                             [BLUE, BLUE, BLUE, BLUE, GREY])
    grey = chromosome_blocks("wxyzE", GREY, [3.0, y, 0], 0.62 * scale,
                             [GREY, GREY, GREY, GREY, TEAL])
    return VGroup(blue, grey)


def translocation_cross():
    """The quadrivalent carried unchanged through pairing, prediction and reveal."""
    arms = VGroup()
    specs = [
        ([-1.25, 0, 0], PI, BLUE, "A B"),
        ([1.25, 0, 0], 0, GREY, "x y"),
        ([0, 1.25, 0], PI / 2, TEAL, "E"),
        ([0, -1.25, 0], -PI / 2, YELLOW, "C D"),
    ]
    for pos, ang, col, txt in specs:
        bar = RoundedRectangle(corner_radius=0.16, width=3.05, height=0.88,
                               stroke_color=col, stroke_width=4,
                               fill_color=col, fill_opacity=0.28)
        lab = T(txt, 34, TEXT, weight=BOLD).move_to(bar)
        arm = VGroup(bar, lab).rotate(ang).move_to(pos)
        arms.add(arm)
    hub = Circle(radius=0.27, color=TEXT, stroke_width=4, fill_color=BG, fill_opacity=1)
    return VGroup(arms, hub)


def small_ledger(title, balanced=True, at=(0, 0, 0)):
    color = GREEN if balanced else RED
    rows = VGroup(
        T("blue blocks  ×1", 25, color),
        T("grey blocks  ×1", 25, color),
    ) if balanced else VGroup(
        T("teal segment  ×2", 25, color),
        T("grey end      ×0", 25, color),
    )
    rows.arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    head = T(title, 27, color, weight=BOLD)
    content = VGroup(head, rows).arrange(DOWN, buff=0.20)
    box = RoundedRectangle(corner_radius=0.16, width=content.width + 0.90,
                           height=content.height + 0.78, color=color, stroke_width=3,
                           fill_color=color, fill_opacity=0.22)
    return VGroup(box, content.move_to(box)).move_to(at)


class S00Hook(SpokenScene):
    def construct(self):
        blue = mini_chromosome(BLUE, -1.0, h=5.1)
        gold = mini_chromosome(YELLOW, 1.0, h=5.1)
        self.at("The first film")
        self.play(FadeIn(blue), FadeIn(gold), run_time=0.8)
        blocks_b = chromosome_blocks(center=[-2.25, 0.15, 0], scale=0.72, vertical=True)
        blocks_y = chromosome_blocks(color=YELLOW, center=[0.0, 0.15, 0], scale=0.72, vertical=True)
        self.play(ReplacementTransform(blue, blocks_b), ReplacementTransform(gold, blocks_y), run_time=1.3)
        bob(blocks_y, amp=0.18, speed=2.2, seed=3)
        v, gauge = dose_meter(0.5, at=[4.5, 0.45, 0], color=GREEN)
        self.add(gauge)
        self.at("Can a chromosome rearrangement")
        q = fit_text("Can rearrangement matter\nwhen no DNA is missing?", max_w=5.4,
                     size=34, color=GOLD).move_to([3.65, 2.95, 0])
        self.play(FadeIn(q), run_time=0.6)
        cut = break_mark(-2.25, 0.72, 1.3).rotate(PI / 2)
        self.play(Create(cut), run_time=0.5)
        self.at("Follow the same")
        self.play(VGroup(blocks_b[2], blocks_b[3], blocks_b[4]).animate.shift(DOWN * 0.3 + RIGHT * 0.3),
                  run_time=1.0)
        finish_alive(self, VGroup(blocks_b, blocks_y))


class S01Title(TitleCard):
    LESSON = "Chromosome number and structure"
    TITLE = "Break, Rejoin, Segregate"


class S02Questions(SpokenScene):
    def construct(self):
        chrom = chromosome_blocks(center=[0.15, 0.35, 0], scale=0.76)
        bob(chrom, amp=0.28, speed=2.8)
        self.at("A chromosome is more")
        self.play(FadeIn(chrom, shift=UP * 0.15), run_time=0.7)
        self.at("Its blocks carry genes")
        self.play(LaggedStart(*[Indicate(b[1], color=TEXT, scale_factor=1.15) for b in chrom],
                              lag_ratio=0.14), run_time=1.1)
        checklist = VGroup(T("DOSE", 31, GREEN, weight=BOLD),
                           T("CONTEXT", 31, TEAL, weight=BOLD),
                           T("MEIOSIS", 31, YELLOW, weight=BOLD)).arrange(DOWN, buff=0.72,
                                                                          aligned_edge=LEFT)
        checklist.move_to([4.7, 0.2, 0])
        self.at("For any rearrangement")
        self.at("what material")
        dv, dg = dose_meter(0.5, at=[-5.1, 0.35, 0], color=GREEN, label="dose")
        self.play(FadeIn(checklist[0]), FadeIn(dg), run_time=0.7)
        self.at("what breakpoint")
        bp = break_mark(chrom[2].get_right()[0] + 0.05, chrom.get_y(), 1.25, TEAL)
        self.play(FadeIn(checklist[1]), Create(bp), run_time=0.7)
        self.at("what products")
        spindle = VGroup(Line([2.3, -1.55, 0], [4.2, -1.55, 0], color=GREY, stroke_width=3),
                         Dot([2.3, -1.55, 0], color=GREY), Dot([4.2, -1.55, 0], color=GREY))
        self.play(FadeIn(checklist[2]), GrowFromCenter(spindle), run_time=0.7)
        finish_alive(self, chrom)


class S03DoseChanges(SpokenScene):
    def construct(self):
        chrom = chromosome_blocks(center=[-2.05, 0.55, 0], scale=0.82)
        v, gauge = dose_meter(0.5, at=[4.7, 0.5, 0], color=RED, label="DNA dose")
        self.add(chrom, gauge, scope_tag("schematic"))
        c = chrom[2]
        self.at("Remove one block")
        self.play(c.animate.shift(UP * 1.65), run_time=0.8)
        self.at("the chromosome has a deletion")
        remaining = VGroup(chrom[0], chrom[1], chrom[3], chrom[4])
        self.play(FadeOut(c), remaining.animate.arrange(RIGHT, buff=BLOCK_GAP * 0.82).move_to([-2.05, 0.55, 0]),
                  v.animate.set_value(0.40), run_time=1.0)
        missing = T("MISSING", 30, RED, weight=BOLD).move_to([4.7, -1.95, 0])
        self.at("Its genes now")
        self.play(FadeIn(missing), run_time=0.4)
        self.at("A missing segment")
        self.play(Indicate(remaining, color=RED), run_time=0.8)
        self.at("Copy one block")
        original = chromosome_blocks(center=[-2.05, 0.55, 0], scale=0.82)
        self.play(FadeOut(remaining), FadeOut(missing), FadeIn(original), v.animate.set_value(0.5), run_time=0.8)
        copy_c = original[2].copy().set_z_index(3)
        self.play(copy_c.animate.shift(UP * 1.65), run_time=0.6)
        self.at("the chromosome has a duplication")
        target = original[2].get_center() + RIGHT * (BLOCK_W * 0.82 + BLOCK_GAP * 0.82)
        self.play(VGroup(original[3], original[4]).animate.shift(RIGHT * (BLOCK_W * 0.82 + BLOCK_GAP * 0.82)),
                  copy_c.animate.move_to(target), v.animate.set_value(0.60), run_time=1.0)
        extra = T("EXTRA", 30, RED, weight=BOLD).move_to([4.7, -1.95, 0])
        self.at("Those genes now")
        self.play(FadeIn(extra), run_time=0.4)
        self.at("An extra segment")
        self.play(Indicate(VGroup(original[2], copy_c), color=RED), run_time=0.8)
        self.at("The red gauge")
        self.play(Indicate(gauge, color=RED), run_time=0.7)
        finish_alive(self, VGroup(original, copy_c))


class S04Inversion(SpokenScene):
    def construct(self):
        chrom = chromosome_blocks(center=[-1.2, 1.0, 0], scale=0.92)
        v, gauge = dose_meter(0.5, at=[4.75, 1.1, 0], color=GREEN, label="balanced dose")
        count = Readout([("chromosomes", lambda: 2, "{:.0f}", GREEN)],
                        at=[4.65, -1.65, 0], widest=[2])
        self.add(chrom, gauge, count)
        group = VGroup(chrom[1], chrom[2], chrom[3])
        self.at("Now cut out")
        self.play(group.animate.shift(UP * 1.25), run_time=0.8)
        self.at("return them in reverse")
        reversed_group = chromosome_blocks("DCB", BLUE, group.get_center(), 0.92)
        self.play(ReplacementTransform(group, reversed_group), run_time=0.9)
        self.at("That is an inversion")
        self.play(reversed_group.animate.shift(DOWN * 1.25), run_time=0.7)
        self.at("No block is lost")
        self.play(Indicate(gauge, color=GREEN), run_time=0.7)
        self.at("chromosome count")
        self.play(Indicate(count, color=GREEN), run_time=0.6)
        self.at("During meiosis")
        self.play(FadeOut(gauge), FadeOut(count), run_time=0.4)
        gold = chromosome_blocks(color=YELLOW, center=[-1.2, -1.0, 0], scale=0.92)
        self.play(FadeIn(gold), run_time=0.5)
        self.at("bend into a loop")
        loop_b = Ellipse(width=7.7, height=2.4, color=BLUE, stroke_width=12).move_to([0, 0, 0])
        loop_y = Ellipse(width=6.5, height=1.55, color=YELLOW, stroke_width=12).move_to([0, 0, 0])
        labels = VGroup(*[T(x, 28, TEXT, weight=BOLD).move_to(p) for x, p in zip(
            "ABCDE", ((-2.8, 0.0, 0), (-1.4, 0.38, 0), (0, 0.50, 0), (1.4, 0.38, 0), (2.8, 0, 0)))])
        self.play(FadeOut(chrom), FadeOut(reversed_group), FadeOut(gold),
                  Create(loop_b), Create(loop_y), FadeIn(labels), run_time=1.4)
        finish_alive(self, VGroup(loop_b, loop_y, labels))


class S05Exchange(SpokenScene):
    def construct(self):
        blue = chromosome_blocks(center=[-3.05, 0.5, 0], scale=0.62)
        grey = chromosome_blocks("wxyzq", GREY, [3.05, 0.5, 0], 0.62)
        v, gauge = dose_meter(0.5, at=[0, -1.75, 0], color=GREEN, label="total dose")
        self.at("A reciprocal translocation")
        self.play(FadeIn(blue), FadeIn(grey), FadeIn(gauge), run_time=0.8)
        bob(blue, amp=0.24, speed=2.5)
        bob(grey, amp=0.20, speed=2.2, seed=2)
        teal_end = blue[4].copy()
        teal_end[0].set_stroke(TEAL).set_fill(TEAL)
        self.at("Move a teal end")
        self.play(FadeOut(blue[4]), FadeIn(teal_end), teal_end.animate.shift(UP * 1.25), run_time=0.9)
        grey_end = grey[4].copy()
        self.at("return a gray segment")
        self.play(FadeOut(grey[4]), FadeIn(grey_end),
                  teal_end.animate.move_to(grey[4]), grey_end.animate.move_to(blue[4]), run_time=1.2)
        final = translocated_pair(y=0.5)
        self.remove(*list(self.mobjects))
        self.add(final, gauge)
        brackets = VGroup(break_mark(final[0][3].get_right()[0] + 0.1, final.get_y(), 0.9),
                          break_mark(final[1][3].get_right()[0] + 0.1, final.get_y(), 0.9))
        pulse(brackets, base=4, amp=1.5, speed=3)
        self.at("Total dose may")
        self.play(Create(brackets), Indicate(gauge, color=GREEN), run_time=0.9)
        finish_alive(self, VGroup(final, brackets))


class S06Context(SpokenScene):
    def construct(self):
        v, gauge = dose_meter(0.5, at=[4.75, 1.55, 0], color=GREEN, label="balanced dose")
        count = Readout([("chromosomes", lambda: 2, "{:.0f}", GREEN)],
                        at=[4.7, -1.25, 0], widest=[2])
        gene = chromosome_blocks("GENE", BLUE, [-1.55, 1.25, 0], 0.78)
        self.at("Balanced dose")
        self.play(FadeIn(gauge), FadeIn(count), FadeIn(gene), run_time=0.8)
        self.at("A breakpoint can interrupt")
        cut = break_mark(gene.get_x(), gene.get_y(), 1.2, TEAL)
        can1 = T("can interrupt", 28, TEAL).move_to([-1.55, 0.15, 0])
        self.play(Create(cut), FadeIn(can1), gene[:2].animate.shift(LEFT * 0.2),
                  gene[2:].animate.shift(RIGHT * 0.2), run_time=0.9)
        self.at("place pieces from different genes")
        a = chromosome_blocks("A", BLUE, [-2.5, -1.4, 0], 0.9)
        b = chromosome_blocks("B", YELLOW, [-0.6, -1.4, 0], 0.9)
        can2 = T("can join", 28, TEAL).move_to([-1.55, -2.5, 0])
        self.play(FadeIn(a), FadeIn(b), FadeIn(can2), run_time=0.8)
        self.at("The result depends")
        self.play(Indicate(VGroup(cut, a, b), color=TEAL), run_time=0.8)
        self.at("changes in gene context")
        rule = caption("Context can change while chromosome count stays the same.", size=28, y=-3.15)
        self.play(FadeOut(can2), FadeIn(rule), Indicate(count, color=GREEN), run_time=0.8)
        finish_alive(self, VGroup(gene, a, b, cut))


class S07Pairing(SpokenScene):
    def construct(self):
        trans = translocated_pair(y=0.3)
        self.at("The carrier still")
        self.play(FadeIn(trans), run_time=0.7)
        normal = VGroup(chromosome_blocks(center=[-3.0, -1.5, 0], scale=0.62),
                        chromosome_blocks("wxyzq", GREY, [3.0, -1.5, 0], 0.62))
        self.at("Normal and translocated")
        self.play(FadeIn(normal), run_time=0.7)
        cross = translocation_cross()
        self.at("All four chromosomes")
        self.play(FadeOut(trans), FadeOut(normal), FadeIn(cross), run_time=1.1)
        zones = VGroup(*[Circle(radius=0.72, color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.16).move_to(p)
                         for p in ((-5.2, 2.35, 0), (5.2, 2.35, 0), (-5.2, -2.35, 0), (5.2, -2.35, 0))])
        self.play(FadeIn(zones), run_time=0.5)
        fibres = VGroup(*[Line(z.get_center(), cross.get_center(), color=GREY, stroke_width=2)
                          for z in zones]).set_opacity(0.65)
        self.at("The way this cross")
        self.play(Create(fibres), run_time=1.0)
        pulse(fibres, base=2, amp=0.7, speed=2)
        finish_alive(self, VGroup(cross, zones, fibres))


class S08Predict(SpokenScene):
    def construct(self):
        cross = translocation_cross()
        zones = VGroup(*[Circle(radius=0.64, color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.16).move_to(p)
                         for p in ((-5.3, 2.25, 0), (5.3, 2.25, 0), (-5.3, -2.25, 0), (5.3, -2.25, 0))])
        marks = VGroup(*[T("?", 34, TEXT).move_to(z) for z in zones])
        self.add(cross, zones, marks)
        bob(cross, amp=0.22, speed=2.5)
        self.at("which separation")
        q = question_card("Which pairing keeps one copy of every block?",
                          [], y=-3.22, size=28, chip_size=25)
        self.play(FadeIn(q), run_time=0.6)
        self.at("opposite chromosomes")
        cross.clear_updaters()
        green = VGroup(DashedLine([-4.2, 2.25, 0], [4.2, -2.25, 0], color=GREEN, stroke_width=5),
                       DashedLine([4.2, 2.25, 0], [-4.2, -2.25, 0], color=GREEN, stroke_width=5))
        glab = T("opposite", 27, GREEN, weight=BOLD).move_to([-4.7, 3.18, 0])
        self.play(Create(green), FadeIn(glab), run_time=0.8)
        self.at("neighboring chromosomes")
        red = VGroup(DashedLine([-4.3, 2.25, 0], [-4.3, -2.25, 0], color=RED, stroke_width=5),
                     DashedLine([4.3, 2.25, 0], [4.3, -2.25, 0], color=RED, stroke_width=5))
        rlab = T("neighbouring", 27, RED, weight=BOLD).move_to([4.55, 3.18, 0])
        self.play(Create(red), FadeIn(rlab), run_time=0.8)
        self.at("Look at the block")
        self.play(Indicate(marks, color=GOLD), run_time=0.8)
        finish_alive(self)


class S09Pause(PredictPause):
    QUESTION = "Which pairing keeps one copy of every block?"
    OPTIONS = []
    CARD = {"y": -3.22, "size": 28, "chip_size": 25}
    SECONDS = 4.5

    def backdrop(self):
        world = question_world(with_question=False)
        bob(world[3], amp=0.18, speed=2.1)
        bob(world[4], amp=0.18, speed=1.9, seed=2)
        return world


class S10Reveal(SpokenScene):
    def construct(self):
        cross = translocation_cross()
        self.add(cross)
        bob(cross, amp=0.22, speed=2.5)
        self.at("Opposite partners")
        arrows = VGroup(Arrow([-1.7, 1.7, 0], [-4.5, 2.35, 0], color=GREEN, buff=0.05),
                        Arrow([1.7, -1.7, 0], [4.5, -2.35, 0], color=GREEN, buff=0.05))
        self.play(*[GrowArrow(a) for a in arrows], run_time=0.8)
        self.at("alternate segregation")
        cross.clear_updaters()
        good = VGroup(small_ledger("normal", True, [-3.7, 0.0, 0]),
                      small_ledger("balanced", True, [3.7, 0.0, 0]))
        self.play(FadeOut(cross), FadeOut(arrows), FadeIn(good), run_time=1.0)
        self.at("Neighboring partners")
        self.play(FadeOut(good), FadeIn(cross), run_time=0.6)
        red_arrows = VGroup(Arrow([-1.7, 1.7, 0], [-4.5, 2.35, 0], color=RED, buff=0.05),
                            Arrow([-1.7, -1.7, 0], [-4.5, -2.35, 0], color=RED, buff=0.05))
        self.play(*[GrowArrow(a) for a in red_arrows], run_time=0.8)
        self.at("an extra copy")
        bad = VGroup(small_ledger("gamete 1", False, [-3.7, 0, 0]),
                     small_ledger("gamete 2", False, [3.7, 0, 0]))
        self.play(FadeOut(cross), FadeOut(red_arrows), FadeIn(bad), run_time=1.0)
        self.at("adjacent segregation")
        cap = caption("Adjacent segregation → unbalanced gametes", color=RED, y=-2.75)
        self.play(FadeIn(cap), Indicate(bad, color=RED), run_time=0.8)
        finish_alive(self, bad)


class S11Carrier(SpokenScene):
    def construct(self):
        carrier = translocated_pair(scale=1.0, y=1.45)
        ledger = small_ledger("balanced carrier", True, [0, -0.05, 0])
        self.at("That explains a common")
        self.play(FadeIn(carrier), FadeIn(ledger), run_time=0.8)
        neutral = VGroup(Circle(radius=0.34, color=GREY, stroke_width=3),
                         Line([0, -0.34, 0], [0, -1.1, 0], color=GREY, stroke_width=3),
                         Line([0, -0.62, 0], [-0.45, -0.95, 0], color=GREY, stroke_width=3),
                         Line([0, -0.62, 0], [0.45, -0.95, 0], color=GREY, stroke_width=3)).move_to([-6.0, 0.55, 0])
        self.at("A carrier can")
        self.play(FadeIn(neutral), Indicate(ledger, color=GREEN), run_time=0.8)
        self.at("Yet meiosis")
        alt = small_ledger("alternate", True, [-3.6, -2.3, 0])
        adj = small_ledger("adjacent", False, [3.6, -2.3, 0])
        self.play(FadeIn(alt), FadeIn(adj), run_time=0.9)
        self.at("Balance must")
        levels = T("carrier level  +  gamete level", 29, GOLD, weight=BOLD).move_to([0, 3.15, 0])
        self.play(FadeIn(levels), run_time=0.6)
        self.at("The rearrangement's consequence")
        self.play(FadeOut(levels), run_time=0.3)
        bp = break_mark(-2.15, 3.12, 0.75, TEAL)
        note = T("outcomes can differ", 27, TEAL).next_to(bp, RIGHT, buff=0.18)
        self.play(Create(bp), FadeIn(note), run_time=0.8)
        finish_alive(self, VGroup(carrier, ledger, neutral, alt, adj))


class S12Rule(SpokenScene):
    def construct(self):
        ledger = small_ledger("balanced carrier", True, [0, 2.35, 0])
        self.add(ledger)
        labels = VGroup(T("DNA DOSE", 31, GREEN, weight=BOLD),
                        T("GENE CONTEXT", 31, TEAL, weight=BOLD),
                        T("MEIOTIC BALANCE", 31, YELLOW, weight=BOLD))
        labels.arrange(RIGHT, buff=1.0).move_to([0, -0.20, 0])
        centers = (-4.35, 0.0, 4.35)
        for lab, x in zip(labels, centers):
            lab.move_to([x, -0.20, 0])
        widths = (3.65, 3.9, 4.4)
        circles = VGroup(*[RoundedRectangle(corner_radius=0.18, width=w, height=1.55,
                                            color=c, stroke_width=4, fill_color=c, fill_opacity=0.18).move_to(l)
                           for l, c, w in zip(labels, (GREEN, TEAL, YELLOW), widths)])
        links = VGroup(Arrow(circles[0].get_right(), circles[1].get_left(), color=GREY, buff=0.12),
                       Arrow(circles[1].get_right(), circles[2].get_left(), color=GREY, buff=0.12))
        self.at("Trace three things")
        self.play(FadeIn(labels), Create(circles), Create(links), run_time=1.0)
        path = VGroup(labels, circles, links)
        bob(path, amp=0.20, speed=2.4)
        self.at("what material was")
        self.play(Indicate(VGroup(circles[0], labels[0]), color=GREEN), run_time=0.8)
        self.at("which genes were")
        self.play(Indicate(VGroup(circles[1], labels[1]), color=TEAL), run_time=0.8)
        self.at("which chromosome combinations")
        self.play(Indicate(VGroup(circles[2], labels[2]), color=YELLOW), run_time=0.8)
        traveler = chromosome_blocks("E", TEAL, [-4.35, -1.65, 0], 0.72)
        self.at("Rearrangements matter")
        self.play(FadeIn(traveler), run_time=0.4)
        self.play(traveler.animate.move_to([0, -1.65, 0]), run_time=0.7)
        self.play(traveler.animate.move_to([4.35, -1.65, 0]), run_time=0.7)
        finish_alive(self)


class S13End(EndCard):
    LINE = "Rearrangements matter through DNA dose, gene context, and meiotic balance."
