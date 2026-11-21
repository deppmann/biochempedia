"""Why dominance does not spread an allele — population-genetics teaching film."""
import numpy as np
from bp_parts import *

P, Q = 0.60, 0.40


def allele_block(kind, w=0.52, h=0.46, label=True):
    """One inherited copy.  A is always blue and a is always gold."""
    color = BLUE if kind == "A" else GOLD
    box = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=color,
                           stroke_width=2.5, fill_color=color, fill_opacity=0.48)
    if not label:
        return box
    return VGroup(box, M(kind, 30, TEXT).move_to(box))


def allele_pair(genotype, gap=0.10):
    return VGroup(*[allele_block(a) for a in genotype]).arrange(RIGHT, buff=gap)


def person(genotype, height=1.65, phenotype=True):
    """Pale person outline with a carried genotype; dominance affects only its rim."""
    dominant = "A" in genotype
    rim = BLUE if phenotype and dominant else (GOLD if phenotype else GREY)
    head = Circle(radius=0.24, stroke_color=GREY, stroke_width=3).shift(UP * 0.53)
    body = RoundedRectangle(corner_radius=0.22, width=1.12, height=1.08,
                            stroke_color=rim, stroke_width=5 if phenotype else 3,
                            fill_color=rim, fill_opacity=0.07).shift(DOWN * 0.25)
    shapes = VGroup(*[allele_block(a, label=False) for a in genotype]).arrange(RIGHT, buff=0.10)
    pair = VGroup(shapes).move_to(body.get_center() + DOWN * 0.03)
    g = VGroup(body, head, pair)
    g.set_height(height)
    letters = VGroup(*[M(a, 24, TEXT).move_to(s) for a, s in zip(genotype, shapes)])
    pair.add(letters)
    g.pair, g.body, g.genotype = pair, body, genotype
    return g


GENOTYPES = ["AA", "AA", "Aa", "Aa", "Aa", "aa"]


def people_row(center=(0, 0.3, 0), height=1.72, phenotype=True):
    row = VGroup(*[person(g, height=height, phenotype=phenotype) for g in GENOTYPES])
    row.arrange(RIGHT, buff=0.38).move_to(center)
    return row


def split_bar(center=(0, -2.35, 0), width=10.4, height=0.78, labels=True, title=None):
    """Computed p/q bar: the boundary is exactly P of the total width."""
    left = center[0] - width / 2
    a = Rectangle(width=width * P, height=height, stroke_color=BLUE, stroke_width=3,
                  fill_color=BLUE, fill_opacity=0.42).move_to([left + width * P / 2, center[1], 0])
    b = Rectangle(width=width * Q, height=height, stroke_color=GOLD, stroke_width=3,
                  fill_color=GOLD, fill_opacity=0.42).move_to([left + width * P + width * Q / 2, center[1], 0])
    g = VGroup(a, b)
    if labels:
        la = M("p = 0.60", 28, BLUE).move_to(a)
        lb = M("q = 0.40", 28, GOLD).move_to(b)
        g.add(la, lb)
    if title:
        g.add(T(title, 28, TEXT).next_to(VGroup(a, b), UP, buff=0.18))
    g.a, g.b = a, b
    return g


def pool(center=(0, 0.35, 0), width=10.8, height=3.75, labels=True):
    """Twenty-copy inventory (12 A, 8 a), built in the same positions every time."""
    frame = RoundedRectangle(corner_radius=0.28, width=width, height=height, stroke_color=GREY,
                             stroke_width=3, fill_color=GREY, fill_opacity=0.025).move_to(center)
    blocks = VGroup()
    for i in range(20):
        kind = "A" if i < 12 else "a"
        blocks.add(allele_block(kind, w=0.56, h=0.48))
    blocks.arrange_in_grid(rows=2, cols=10, buff=(0.34, 0.58)).move_to(center)
    g = VGroup(frame, blocks)
    if labels:
        lab = T("population allele copies", 30, TEXT).next_to(frame, UP, buff=0.20)
        g.add(lab)
    g.frame, g.blocks = frame, blocks
    return g


def genotype_cards(center=(0, -1.65, 0), scale=1.0):
    cards = VGroup()
    for gt in ("AA", "Aa", "aa"):
        col = BLUE if "A" in gt else GOLD
        box = RoundedRectangle(corner_radius=0.18, width=2.25, height=1.25, stroke_color=col,
                               stroke_width=4, fill_color=col, fill_opacity=0.10)
        pair = allele_pair(gt).scale(0.82).move_to(box.get_center() + UP * 0.13)
        lab = M(gt, 28, col).next_to(pair, DOWN, buff=0.09)
        cards.add(VGroup(box, pair, lab))
    cards.arrange(RIGHT, buff=0.55).scale(scale).move_to(center)
    return cards


def gamete_lanes():
    """Same 60:40 split in egg and sperm lanes."""
    lanes = VGroup()
    for name, y in (("egg lane", 1.55), ("sperm lane", -0.45)):
        frame = RoundedRectangle(corner_radius=0.2, width=9.8, height=1.28, stroke_color=GREY,
                                 stroke_width=3).move_to([0, y, 0])
        copies = VGroup(*[allele_block("A" if i < 6 else "a", w=0.45, h=0.42) for i in range(10)])
        copies.arrange(RIGHT, buff=0.18).move_to([0.72, y, 0])
        label_y = y + (0.36 if name == "egg lane" else 0.91)
        label = T(name, 28, TEXT).move_to([-4.02, label_y, 0])
        lane = VGroup(frame, copies, label)
        lane.copies = copies
        lanes.add(lane)
    return lanes


def probability_square(center=(-0.65, -0.25, 0), side=5.55, labels=False):
    """Area model computed from p=.60 and q=.40; rows are sperm, columns eggs."""
    x0, y1 = center[0] - side / 2, center[1] + side / 2
    wp, wq, hp, hq = side * P, side * Q, side * P, side * Q
    specs = [
        ("AA", x0, y1 - hp, wp, hp, BLUE),
        ("Aa_top", x0 + wp, y1 - hp, wq, hp, TEAL),
        ("Aa_bottom", x0, y1 - hp - hq, wp, hq, TEAL),
        ("aa", x0 + wp, y1 - hp - hq, wq, hq, GOLD),
    ]
    cells = {}
    g = VGroup()
    for name, x, y, w, h, color in specs:
        r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=4,
                      fill_color=color, fill_opacity=0.28).move_to([x + w / 2, y + h / 2, 0])
        cells[name] = r
        g.add(r)
    if labels:
        texts = {"AA": ("AA   p²", BLUE), "Aa_top": ("Aa   pq", TEAL),
                 "Aa_bottom": ("Aa   qp", TEAL), "aa": ("aa   q²", GOLD)}
        for key, (txt, col) in texts.items():
            g.add(M(txt, 27, col).move_to(cells[key]))
    g.cells = cells
    return g


def lane_question_world():
    lanes = gamete_lanes()
    q = question_card("What happens to p?", ["higher", "lower", "unchanged"],
                      y=-3.23, chips_at=[4.75, -1.42, 0], max_w=5.8, left=-5.95)
    return VGroup(lanes, q)


def eye_icon(center=(-4.85, 2.4, 0), width=1.9):
    eye = Ellipse(width=width, height=0.95, stroke_color=TEXT, stroke_width=4).move_to(center)
    iris = Circle(radius=0.24, color=BLUE, fill_color=BLUE, fill_opacity=0.55).move_to(center)
    return VGroup(eye, iris)


class S00Hook(SpokenScene):
    def construct(self):
        question = T("Why not everyone?", 42, TEXT, font=TITLE_FONT).move_to([0, 3.28, 0])
        self.at("A dominant allele")
        row = people_row(center=(0, 0.85, 0), height=2.0)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.12) for p in row], lag_ratio=0.08), run_time=1.7)
        for p in row:
            bob(p.pair, amp=0.035, speed=1.8, seed=len(p.genotype))
        hw = boxed_label("already at Hardy-Weinberg proportions", GREY, size=25).move_to([0, -1.22, 0])
        self.play(FadeIn(hw), run_time=0.55)
        self.at("Why does it not spread")
        self.play(FadeIn(question, shift=DOWN * 0.1), run_time=0.65)
        bar = split_bar(center=(0, -2.35, 0), width=10.2, height=0.7, labels=False)
        self.play(FadeIn(bar), run_time=0.55)
        predicted = DashedLine(bar.a.get_corner(UR), [5.10, -0.93, 0], color=TEXT, stroke_width=4)
        pred_lab = T("predicted?", 27, TEXT).move_to([3.55, -0.45, 0])
        everyone = T("everyone", 27, GREY).move_to([5.35, -0.80, 0])
        self.play(Create(predicted), FadeIn(pred_lab), FadeIn(everyone), run_time=0.9)
        self.at("Follow the allele copies")
        self.play(FadeOut(VGroup(predicted, pred_lab, everyone, hw)),
                  Indicate(VGroup(*[p.pair for p in row]), color=TEXT, scale_factor=1.08), run_time=1.1)
        self.at("Their count")
        count = M("12 A  +  8 a", 36, TEXT).move_to([0, -1.35, 0])
        self.play(FadeIn(count), bar.a.animate.set_fill(BLUE, 0.65), bar.b.animate.set_fill(GOLD, 0.65), run_time=0.8)
        self.finish()


class S01Title(NarratedScene):
    def construct(self):
        row = people_row(center=(0, 0.15, 0), height=1.7).set_opacity(0.28)
        for p in row:
            bob(p.pair, amp=0.035, speed=1.7, seed=1)
        question = T("Why not everyone?", 31, GREY).move_to([0, -2.05, 0]).set_opacity(0.55)
        title = fit_text("Why Dominance Does Not Spread an Allele", max_w=11.4, size=50,
                         min_size=36, font=TITLE_FONT).move_to([0, 2.25, 0])
        rule = Line(LEFT * 1.3, RIGHT * 1.3, color=GOLD, stroke_width=4).next_to(title, DOWN, buff=0.25)
        self.add(row, question)
        self.play(Write(title), GrowFromCenter(rule), run_time=1.05)
        self.finish()


class S02Copies(SpokenScene):
    def construct(self):
        row = people_row(center=(0, 1.6, 0), height=1.28, phenotype=False)
        self.at("Each person holds")
        self.play(FadeIn(row), run_time=0.9)
        brace = Brace(row[2].pair, DOWN, color=TEXT)
        glab = T("one genotype", 28, TEXT).next_to(brace, DOWN, buff=0.12)
        self.play(GrowFromCenter(brace), FadeIn(glab), run_time=0.65)
        self.at("Population genetics")
        self.play(FadeOut(VGroup(brace, glab)), row.animate.shift(UP * 0.45).set_opacity(0.42), run_time=0.6)
        po = pool(center=(0, -0.15, 0), width=11.2, height=2.65)
        po[2].next_to(po.frame, DOWN, buff=0.16)
        self.play(Create(po.frame), run_time=0.5)
        self.at("Across everyone")
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.25) for b in po.blocks], lag_ratio=0.025),
                  FadeIn(po[2]), run_time=1.7)
        self.at("what fraction")
        bar = split_bar(center=(0, -2.65, 0), width=10.9, height=0.72, labels=True)
        self.play(GrowFromEdge(bar.a, LEFT), run_time=0.8)
        self.at("That fraction")
        self.play(FadeIn(VGroup(bar.b, bar[2], bar[3])), run_time=0.75)
        self.at("An individual")
        self.play(row.animate.set_opacity(0.16), Indicate(VGroup(po.blocks, bar), color=TEXT, scale_factor=1.025), run_time=1.0)
        self.finish()


class S03SameInventory(SpokenScene):
    def construct(self):
        po = pool(center=(0, 1.02, 0), width=11.3, height=3.25)
        for i, b in enumerate(po.blocks):
            bob(b, amp=0.055, speed=1.4 + 0.04 * i, seed=i)
        bar = split_bar(center=(0, -1.1, 0), width=10.6, height=0.72, labels=True)
        self.at("The pool contains")
        self.play(FadeIn(po), run_time=0.9)
        self.at("Their fractions")
        self.play(FadeIn(bar), run_time=0.75)
        lock = T("same copies", 28, TEXT).next_to(bar, DOWN, buff=0.16)
        self.at("Together")
        self.play(FadeIn(lock), Indicate(bar, color=TEXT, scale_factor=1.02), run_time=0.75)
        self.at("Dominance changes")
        self.play(FadeOut(po), bar.animate.shift(UP * 2.65).scale(0.78), FadeOut(lock), run_time=0.75)
        cards = genotype_cards(center=(0, -0.65, 0), scale=1.15)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cards], lag_ratio=0.18), run_time=1.2)
        visible = T("dominant trait visible", 30, BLUE).move_to([0, -2.05, 0])
        self.play(FadeIn(visible), Indicate(VGroup(cards[0], cards[1]), color=BLUE, scale_factor=1.04), run_time=0.9)
        self.at("but it adds no")
        same = M("A copies: unchanged", 34, TEXT).move_to([0, -2.75, 0])
        self.play(FadeIn(same), run_time=0.6)
        self.at("inheritance")
        self.play(Indicate(bar, color=TEXT, scale_factor=1.04), cards.animate.set_opacity(0.55), run_time=0.8)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        lanes = gamete_lanes()
        self.at("Now let eggs")
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in lanes], lag_ratio=0.2), run_time=1.1)
        for j, lane in enumerate(lanes):
            bob(lane.copies, amp=0.05, speed=1.35, seed=j)
        gates = VGroup(*[Line([5.15, y - 0.42, 0], [5.15, y + 0.42, 0], color=TEAL, stroke_width=7)
                         for y in (1.55, -0.45)])
        self.play(FadeIn(gates), run_time=0.55)
        self.at("Before they pair")
        prompt = question_card("What happens to p?", ["higher", "lower", "unchanged"],
                               y=-3.23, max_w=5.8, left=-5.55)
        self.play(FadeIn(prompt.question), run_time=0.55)
        self.at("Does random pairing")
        self.play(LaggedStart(*[FadeIn(c, shift=LEFT * 0.15) for c in prompt.chips], lag_ratio=0.16), run_time=1.0)
        self.at("Keep your eye")
        self.play(Indicate(VGroup(*[l.copies for l in lanes]), color=TEXT, scale_factor=1.025), run_time=0.8)
        self.finish()


class S05PredictPause(PredictPause):
    QUESTION = "What happens to p?"
    OPTIONS = ["higher", "lower", "unchanged"]
    CHIPS_AT = None
    CARD = {"y": -3.23, "max_w": 5.8, "left": -5.55}
    RING_AT = (6.05, -3.18, 0)
    SECONDS = 4.5

    def backdrop(self):
        lanes = gamete_lanes()
        for j, lane in enumerate(lanes):
            bob(lane.copies, amp=0.05, speed=1.35, seed=j)
        gates = VGroup(*[Line([5.15, y - 0.42, 0], [5.15, y + 0.42, 0], color=TEAL, stroke_width=7)
                         for y in (1.55, -0.45)])
        pulse(gates, base=7, amp=1.2, speed=2.6)
        return VGroup(lanes, gates)


class S06RandomPairing(SpokenScene):
    def construct(self):
        sq = probability_square(labels=False)
        heads = VGroup(M("egg: A  0.60", 27, BLUE), M("egg: a  0.40", 27, GOLD)).arrange(RIGHT, buff=0.75)
        heads.move_to([-0.65, 3.18, 0])
        sides = VGroup(M("sperm A\n0.60", 26, BLUE), M("sperm a\n0.40", 26, GOLD))
        sides[0].move_to([-4.55, 0.72, 0]); sides[1].move_to([-4.55, -1.98, 0])
        self.at("Random means")
        self.play(FadeIn(heads), FadeIn(sides), Create(VGroup(*sq.cells.values()).set_fill(opacity=0)), run_time=1.2)
        self.at("Draw blue from both")
        aa = M("AA", 36, BLUE).move_to(sq.cells["AA"])
        self.play(sq.cells["AA"].animate.set_fill(BLUE, 0.35), FadeIn(aa), run_time=0.85)
        cursor1 = SurroundingRectangle(heads[0], color=TEXT, buff=0.08)
        cursor2 = SurroundingRectangle(sides[0], color=TEXT, buff=0.08)
        self.play(Create(cursor1), Create(cursor2), run_time=0.5)
        self.at("Draw unlike")
        mixed = VGroup(sq.cells["Aa_top"], sq.cells["Aa_bottom"])
        mixlabs = VGroup(*[M("Aa", 34, TEAL).move_to(c) for c in mixed])
        self.play(FadeOut(VGroup(cursor1, cursor2)), mixed.animate.set_fill(TEAL, 0.35), FadeIn(mixlabs), run_time=0.9)
        self.at("in either order")
        self.play(Indicate(mixed, color=TEXT, scale_factor=1.025), run_time=0.65)
        self.at("Draw gold from both")
        al = M("aa", 36, GOLD).move_to(sq.cells["aa"])
        self.play(sq.cells["aa"].animate.set_fill(GOLD, 0.35), FadeIn(al), run_time=0.85)
        self.at("No draw remembers")
        no_memory = boxed_label("copies, not phenotype", TEXT, size=28).move_to([4.35, -2.25, 0])
        self.play(FadeIn(no_memory), run_time=0.75)
        self.finish()


class S07Proportions(SpokenScene):
    def construct(self):
        bar = split_bar(center=(0, 3.08, 0), width=8.4, height=0.48, labels=True)
        sq = probability_square(center=(-0.75, -0.35, 0), side=5.45, labels=False)
        for cell in sq.cells.values():
            pulse(cell, base=4.0, amp=1.4, speed=1.7)
        title = T("genotype proportions", 30, TEXT).move_to([4.45, 2.28, 0])
        self.at("The square gives")
        self.play(FadeIn(bar), Create(VGroup(*sq.cells.values())), FadeIn(title), run_time=1.2)
        self.at("Blue homozygotes")
        l1 = M("p²", 38, TEXT).move_to(sq.cells["AA"])
        self.play(FadeIn(l1), sq.cells["AA"].animate.set_fill(BLUE, 0.62), run_time=0.75)
        self.at("Heterozygotes")
        l2 = M("pq", 34, TEXT).move_to(sq.cells["Aa_top"])
        l3 = M("qp", 34, TEXT).move_to(sq.cells["Aa_bottom"])
        self.play(FadeIn(l2), FadeIn(l3),
                  sq.cells["Aa_top"].animate.set_fill(TEAL, 0.62),
                  sq.cells["Aa_bottom"].animate.set_fill(TEAL, 0.62), run_time=0.9)
        self.at("Gold homozygotes")
        l4 = M("q²", 38, TEXT).move_to(sq.cells["aa"])
        self.play(FadeIn(l4), sq.cells["aa"].animate.set_fill(GOLD, 0.62), run_time=0.75)
        self.at("Together")
        total = M("p² + 2pq + q² = 1", 30, TEXT).move_to([4.5, 0.15, 0])
        self.play(FadeOut(VGroup(l2, l3)), FadeIn(total), run_time=0.75)
        mix = boxed_label("Aa = 2pq", TEAL, size=30).move_to([4.35, -1.15, 0])
        self.play(FadeIn(mix), run_time=0.65)
        self.at("These areas describe")
        people = T("people", 32, TEXT).move_to([4.35, -2.25, 0])
        copies = T("not new copies", 30, GREY).next_to(people, DOWN, buff=0.18)
        self.play(FadeIn(people), FadeIn(copies), title.animate.set_color(GREY), run_time=0.75)
        self.finish()


class S08Recount(SpokenScene):
    def construct(self):
        sq = probability_square(center=(-2.65, 1.85, 0), side=2.45, labels=False)
        cards = genotype_cards(center=(-2.65, 2.20, 0), scale=0.88)
        released = VGroup(
            VGroup(allele_block("A", w=0.52, h=0.46), allele_block("A", w=0.52, h=0.46)).arrange(RIGHT, buff=0.10),
            VGroup(allele_block("A", w=0.52, h=0.46), allele_block("a", w=0.52, h=0.46)).arrange(RIGHT, buff=0.10),
            VGroup(allele_block("a", w=0.52, h=0.46), allele_block("a", w=0.52, h=0.46)).arrange(RIGHT, buff=0.10),
        )
        for pair, card in zip(released, cards):
            pair.move_to(card.get_bottom() + DOWN * 0.44)

        self.at("Recount blue")
        sq_aa = sq.cells["AA"]
        sq_het = VGroup(sq.cells["Aa_top"], sq.cells["Aa_bottom"])
        sq_aa_gold = sq.cells["aa"]
        self.play(FadeIn(sq_aa), FadeIn(sq_het), FadeIn(sq_aa_gold), run_time=0.55)
        self.play(
            ReplacementTransform(sq_aa, cards[0]),
            ReplacementTransform(sq_het, cards[1]),
            ReplacementTransform(sq_aa_gold, cards[2]),
            run_time=0.85,
        )
        for i, c in enumerate(cards):
            bob(c, amp=0.03, speed=1.4, seed=i)
        self.play(
            LaggedStart(*[FadeIn(p, shift=DOWN * 0.25) for p in released], lag_ratio=0.15),
            run_time=0.75,
        )

        # Algebra derivation on the upper-right, built term-by-term with the voice.
        alg_x = 1.45
        t_p2 = M("p²", 32, BLUE).move_to([alg_x, 2.78, 0], aligned_edge=LEFT)
        t_plus = M("+", 32, TEXT).next_to(t_p2, RIGHT, buff=0.18)
        t_2pq = M("2pq", 32, TEAL).next_to(t_plus, RIGHT, buff=0.18)
        t_half = M("1/2(2pq)", 32, TEAL).next_to(t_plus, RIGHT, buff=0.18)
        t_eq_pq = M("= pq", 26, TEAL).next_to(t_half, DOWN, buff=0.16)

        self.at("Blue homozygotes")
        self.play(Indicate(cards[0], color=BLUE), Indicate(released[0], color=BLUE), run_time=0.7)

        self.at("giving p squared")
        self.play(FadeIn(t_p2), run_time=0.55)

        self.at("Heterozygotes make up")
        self.play(Indicate(cards[1], color=TEAL), Indicate(released[1], color=TEAL), run_time=0.55)

        self.at("2pq")
        self.play(FadeIn(t_plus), FadeIn(t_2pq), run_time=0.5)

        self.at("are half blue")
        self.play(
            ReplacementTransform(t_2pq, t_half),
            Indicate(released[1][0], color=BLUE, scale_factor=1.15),
            released[1][1].animate.set_opacity(0.35),
            run_time=0.55,
        )

        self.at("giving pq")
        self.play(FadeIn(t_eq_pq), run_time=0.5)

        # Stream blocks into the new bar and show the combined expression p² + pq.
        bar_x, bar_w, bar_h = -2.35, 7.0, 0.50
        before = split_bar(center=(bar_x, -0.82, 0), width=bar_w, height=bar_h, labels=False, title="before")
        after = split_bar(center=(bar_x, -2.55, 0), width=bar_w, height=bar_h, labels=False)
        after.a.set_fill(BLUE, 0.05)
        after.b.set_fill(GOLD, 0.05)
        after_label = T("next generation", 26, TEXT).next_to(after, DOWN, buff=0.16)

        stream = VGroup()
        blue_targets, gold_targets = [], []
        a_left = after.a.get_left()[0] + 0.35
        a_step = (after.a.width - 0.7) / 11.0
        b_left = after.b.get_left()[0] + 0.35
        b_step = (after.b.width - 0.7) / 7.0
        # 12 blue (7 from AA, 5 from Aa) and 8 gold (5 from Aa, 3 from aa) match p=0.60, q=0.40.
        sources = (
            [("A", released[0])] * 7
            + [("A", released[1])] * 5
            + [("a", released[1])] * 5
            + [("a", released[2])] * 3
        )
        b_idx = g_idx = 0
        for kind, src in sources:
            blk = allele_block(kind, w=0.34, h=0.30, label=False).move_to(src)
            stream.add(blk)
            if kind == "A":
                blue_targets.append(np.array([a_left + a_step * b_idx, after.get_center()[1], 0]))
                b_idx += 1
            else:
                gold_targets.append(np.array([b_left + b_step * g_idx, after.get_center()[1], 0]))
                g_idx += 1
        all_targets = blue_targets + gold_targets

        eq_sum = M("= p² + pq", 32, TEXT).move_to([alg_x, 1.55, 0], aligned_edge=LEFT)

        pred_title = T("prediction", 25, TEXT).move_to([4.45, -1.05, 0])
        pred_chips = VGroup(*[chip(o, TEXT, 24, pad=0.16) for o in ("higher", "lower", "unchanged")])
        pred_chips.arrange(DOWN, buff=0.16, aligned_edge=LEFT).next_to(pred_title, DOWN, buff=0.22)

        self.at("Adding them gives")
        self.add(stream)
        self.play(
            FadeIn(before),
            FadeIn(after),
            FadeIn(after_label),
            FadeIn(eq_sum),
            FadeIn(pred_title),
            FadeIn(pred_chips),
            LaggedStart(*[b.animate.move_to(t) for b, t in zip(stream, all_targets)], lag_ratio=0.03),
            run_time=1.4,
        )
        self.play(
            FadeOut(stream),
            after.a.animate.set_fill(BLUE, 0.42),
            after.b.animate.set_fill(GOLD, 0.42),
            run_time=0.45,
        )

        # Factor to p(p + q).
        eq_factor = M("= p(p + q)", 32, TEXT).move_to([alg_x, 0.85, 0], aligned_edge=LEFT)
        eq_factor_gold = M("= p(p + q)", 32, TEXT, t2c={"p + q": GOLD}).move_to(eq_factor)

        self.at("factors to")
        self.play(FadeIn(eq_factor, shift=DOWN * 0.22), run_time=0.8)

        # Highlight p + q = 1 as spoken (do not show 1 until spoken).
        pq_note_lhs = boxed_label("p + q", GOLD, size=26).move_to([5.15, 0.85, 0])
        pq_note_full = boxed_label("p + q = 1", GOLD, size=26).move_to([5.15, 0.85, 0])

        self.at("Since p plus q")
        self.remove(eq_factor)
        self.add(eq_factor_gold)
        self.play(FadeIn(pq_note_lhs), Indicate(eq_factor_gold, color=GOLD, scale_factor=1.03), run_time=0.5)

        self.at("equals 1")
        self.play(ReplacementTransform(pq_note_lhs, pq_note_full), run_time=0.4)

        # Return to p, slide new bar under original, and outline "unchanged".
        eq_final = M("= p", 38, BLUE).move_to([alg_x, 0.12, 0], aligned_edge=LEFT)
        shift_up = UP * 0.88
        after_target_split_x = after.a.get_right()[0]
        match_line = DashedLine(
            [after_target_split_x, before.get_bottom()[1], 0],
            [after_target_split_x, after.get_top()[1] + shift_up[1], 0],
            color=TEXT,
            stroke_width=4,
            dash_length=0.09,
        )
        unchanged_outline = SurroundingRectangle(pred_chips[2], color=TEXT, buff=0.09, stroke_width=4)

        self.at("the share returns to p")
        self.play(
            FadeIn(eq_final, shift=DOWN * 0.20),
            VGroup(after, after_label).animate.shift(shift_up),
            run_time=0.9,
        )
        self.play(
            Create(match_line),
            pred_chips[0][0].animate.set_stroke(opacity=0.25).set_fill(opacity=0.04),
            pred_chips[0][1].animate.set_opacity(0.28),
            pred_chips[1][0].animate.set_stroke(opacity=0.25).set_fill(opacity=0.04),
            pred_chips[1][1].animate.set_opacity(0.28),
            Create(unchanged_outline),
            run_time=0.65,
        )
        pulse(unchanged_outline, base=4.0, amp=1.2, speed=2.2)

        self.at("Random mating changed")
        self.play(Indicate(cards, color=TEAL), run_time=0.7)

        self.at("not the allele frequency")
        self.play(Indicate(VGroup(before, after, unchanged_outline), color=TEXT, scale_factor=1.02), run_time=0.8)
        self.finish()


class S09Dominance(SpokenScene):
    def construct(self):
        row = people_row(center=(0, 0.72, 0), height=1.7, phenotype=True)
        self.at("Dominance still")
        self.play(LaggedStart(*[FadeIn(p) for p in row], lag_ratio=0.08), run_time=1.0)
        self.at("Both blue homozygotes")
        eye = eye_icon(center=(-4.9, 2.65, 0))
        count = M("5 visible", 30, BLUE).next_to(eye, RIGHT, buff=0.25)
        self.play(FadeIn(eye), FadeIn(count), Indicate(VGroup(*row[:5]), color=BLUE, scale_factor=1.025), run_time=0.9)
        self.at("Yet visibility")
        bar = split_bar(center=(0, -1.55, 0), width=10.4, height=0.72, labels=True)
        self.play(FadeIn(bar), run_time=0.7)
        self.at("A visible effect")
        proposal = Arrow([-3.8, -2.72, 0], [3.75, -2.72, 0], color=BLUE, stroke_width=7, buff=0)
        shortcut = T("extra copying route?", 29, BLUE).next_to(proposal, DOWN, buff=0.16)
        self.play(GrowArrow(proposal), FadeIn(shortcut), run_time=0.75)
        no = M("×", 64, RED).move_to(proposal)
        self.play(FadeIn(no, scale=1.25), proposal.animate.set_opacity(0.18), shortcut.animate.set_opacity(0.25), run_time=0.65)
        self.at("Without unequal survival")
        forces = VGroup(*[boxed_label(s, RED, size=25) for s in ("survival", "reproduction", "other force")])
        forces.arrange(RIGHT, buff=0.35).move_to([0, -3.15, 0])
        self.play(FadeOut(VGroup(proposal, shortcut, no)), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(x) for x in forces], lag_ratio=0.15), run_time=0.6)
        self.at("no extra")
        self.play(FadeOut(forces), Indicate(bar, color=TEXT, scale_factor=1.025), run_time=0.7)
        self.finish()


class S10NullModel(SpokenScene):
    def construct(self):
        expected = [P * P, 2 * P * Q, Q * Q]
        labels = ["AA", "Aa", "aa"]
        cols = [BLUE, TEAL, GOLD]
        base, scale = -2.25, 8.0
        axes = Line([-5.8, base, 0], [1.0, base, 0], color=GREY, stroke_width=3)
        bars = VGroup()
        outlines = VGroup()
        for x, val, lab, col in zip((-4.65, -2.35, -0.05), expected, labels, cols):
            r = Rectangle(width=0.92, height=val * scale, stroke_color=TEXT, stroke_width=4,
                          fill_color=col, fill_opacity=0.32).move_to([x, base + val * scale / 2, 0])
            bars.add(VGroup(r, M(lab, 28, col).move_to([x, base - 0.38, 0])))
            outlines.add(Rectangle(width=0.92, height=val * scale, stroke_color=GREY, stroke_width=2,
                                   fill_opacity=0).move_to(r))
        for outline in outlines:
            pulse(outline, base=2.0, amp=0.8, speed=1.6)
        bob(bars, amp=0.035, speed=1.3)
        self.at("This is a baseline")
        baseline = boxed_label("Hardy-Weinberg baseline", TEXT, size=30).move_to([-2.4, 3.16, 0])
        pulse(baseline.box, base=2.5, amp=1.0, speed=1.8)
        self.play(FadeIn(baseline), Create(axes), run_time=0.75)
        self.play(LaggedStart(*[Create(o) for o in outlines], lag_ratio=0.28), run_time=2.4)
        self.at("It assumes")
        assumptions = VGroup(*[boxed_label(s, GREY, size=25) for s in
                               ("large population", "random mating", "no force on copies")])
        assumptions.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([4.25, 1.65, 0])
        bob(assumptions, amp=0.04, speed=1.25)
        self.play(Indicate(outlines, color=TEXT, scale_factor=1.02), run_time=0.45)
        self.at("large population")
        self.play(FadeIn(assumptions[0], shift=LEFT * 0.5), run_time=0.55)
        self.at("random mating")
        self.play(FadeIn(assumptions[1], shift=LEFT * 0.5), run_time=0.55)
        self.at("no force")
        self.play(FadeIn(assumptions[2], shift=LEFT * 0.5), run_time=0.55)
        self.at("Hardy Weinberg predicts")
        self.play(LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars], lag_ratio=0.18),
                  FadeIn(VGroup(*[b[1] for b in bars])), run_time=1.25)
        bracket = Brace(VGroup(*[b[0] for b in bars]), UP, color=TEXT)
        null = T("null expectation", 29, TEXT).next_to(bracket, UP, buff=0.12)
        self.play(GrowFromCenter(bracket), FadeIn(null), run_time=0.65)
        self.at("testable expectation")
        observed = VGroup()
        for x, val in zip((-4.65, -2.35, -0.05), (0.31, 0.54, 0.15)):
            r = Rectangle(width=0.52, height=val * scale, stroke_color=GREY, stroke_width=3,
                          fill_color=GREY, fill_opacity=0.38).move_to([x + 0.72, base + val * scale / 2, 0])
            observed.add(r)
        self.play(LaggedStart(*[GrowFromEdge(r, DOWN) for r in observed], lag_ratio=0.16), run_time=1.0)
        self.at("Data can then depart")
        outside = VGroup(*[boxed_label(s, RED, size=24) for s in ("selection", "migration", "mutation", "drift")])
        outside.arrange_in_grid(rows=2, cols=2, buff=(0.35, 0.28)).move_to([4.25, -1.55, 0])
        bob(outside, amp=0.04, speed=1.3)
        self.play(FadeOut(assumptions),
                  LaggedStart(*[FadeIn(x) for x in outside], lag_ratio=0.12), run_time=0.9)
        self.add(scope_tag("schematic"))
        self.finish()


class S11Rule(SpokenScene):
    def construct(self):
        row = people_row(center=(0, 2.15, 0), height=1.30, phenotype=False)
        po = pool(center=(0, 0.25, 0), width=9.6, height=1.55, labels=False)
        po.blocks.move_to(po.frame)
        pulse(po.frame, base=3.0, amp=1.5, speed=1.5)
        bar = split_bar(center=(0, -1.25, 0), width=9.8, height=0.7, labels=True)
        self.at("answer the opening")
        self.play(FadeIn(row), FadeIn(po), run_time=0.9)
        self.at("counting copies")
        self.play(FadeIn(bar), Indicate(po.blocks, color=TEXT, scale_factor=1.025), run_time=0.8)
        self.at("Mating reshuffles")
        reshuffle = T("mating reshuffles", 32, TEAL).move_to([-3.3, -2.45, 0])
        self.play(FadeIn(reshuffle), Rotate(po.blocks, angle=0.06, rate_func=there_and_back), run_time=0.75)
        self.at("Dominance alone")
        fixed = T("frequency unchanged", 32, TEXT).move_to([2.7, -2.45, 0])
        boundary = Line(bar.a.get_right() + UP * 0.48, bar.a.get_right() + DOWN * 0.48,
                        color=TEXT, stroke_width=7)
        self.play(FadeIn(fixed), Create(boundary), run_time=0.75)
        self.at("A changing allele bar")
        force = Arrow([4.8, 3.1, 0], [4.8, -0.65, 0], color=RED, stroke_width=8, buff=0.15)
        flab = boxed_label("force changes copies", RED, size=27).move_to([4.55, 3.25, 0])
        self.play(FadeIn(flab), GrowArrow(force), run_time=0.9)
        self.at("enter the next generation")
        self.play(force.animate.shift(DOWN * 0.18), Indicate(bar, color=RED, scale_factor=1.02), run_time=0.7)
        self.finish()


class S12End(EndCard):
    LINE = "Mating reshuffles alleles; dominance alone does not change their frequency."
