"""The Marker in the Middle.

COLOUR MAP
  BLUE  = one parental chromosome / allele pattern
  GOLD  = the other parental chromosome / allele pattern
  GREEN = the middle marker
  RED   = crossover points and double-crossover counters
  GREY  = tester material, shutters, and secondary structure
  TEXT  = neutral labels

The ribbon, pattern-card, and map builders are shared by every continuing scene so
the film stays in one visual world at a fixed scale and position.
"""
from bp_parts import *


RIBBON_X = (-4.8, 0.0, 4.8)
RIBBON_Y = (1.25, -1.25)
CARD_Y = (1.15, -1.25)


def marker_block(letter, color, x, y, middle=False, fill=None, scale=1.0):
    """A large allele block; GREEN is reserved for the middle-marker outline."""
    edge = GREEN if middle else color
    fc = color if fill is None else fill
    box = RoundedRectangle(
        corner_radius=0.12,
        width=max(0.65, 1.35 * scale),
        height=max(0.58, 1.02 * scale),
        stroke_color=edge,
        stroke_width=5 if middle else 3,
        fill_color=fc,
        fill_opacity=0.55,
    ).move_to([x, y, 0])
    lab = M(letter, max(22, 34 * scale), TEXT).move_to(box)
    lab.add_background_rectangle(color=BG, opacity=0.78, buff=0.05)
    return VGroup(box, lab)


def ribbon_row(y, color, alleles=("A", "C", "B"), fills=None, show_middle=True, xshift=0):
    """One carried chromosome ribbon with three fixed marker slots."""
    # Leave real gaps behind the marker blocks.  This keeps the ribbon from
    # crossing letters while reading as one continuous chromosome.
    edges = (-5.7, -5.5, -4.1, -0.7, 0.7, 4.1, 5.5, 5.7)
    line = VGroup(*[
        Line([edges[i] + xshift, y, 0], [edges[i + 1] + xshift, y, 0], color=color, stroke_width=44)
        for i in (0, 2, 4, 6)
    ]).set_opacity(0.55)
    fills = fills or (color, color, color)
    blocks = VGroup()
    for i, (x, a, fc) in enumerate(zip(RIBBON_X, alleles, fills)):
        b = marker_block(a, color, x + xshift, y, middle=(i == 1), fill=fc)
        if i == 1 and not show_middle:
            b.set_opacity(0)
        blocks.add(b)
    return VGroup(line, blocks)


def chromosome_world(show_middle=True, product=False, labels=False, drift=False):
    """The film's two-ribbon world, rebuilt identically throughout."""
    top_fills = (BLUE, GOLD if product else BLUE, BLUE)
    bot_fills = (GOLD, BLUE if product else GOLD, GOLD)
    top = ribbon_row(RIBBON_Y[0], BLUE, fills=top_fills, show_middle=show_middle)
    bot = ribbon_row(RIBBON_Y[1], GOLD, fills=bot_fills, show_middle=show_middle)
    g = VGroup(top, bot)
    if labels:
        left = T("left", 28, TEXT).move_to([RIBBON_X[0], 2.25, 0])
        right = T("right", 28, TEXT).move_to([RIBBON_X[2], 2.25, 0])
        g.add(left, right)
    if drift:
        bob(g, amp=0.045, speed=0.65)
    return g


def breathe_ribbons(world):
    """Continuous visible motion on the chromosome itself, not a decorative overlay."""
    for r, row in enumerate(world[:2]):
        for i, segment in enumerate(row[0]):
            pulse(segment, base=44, amp=5.5, speed=1.35 + 0.08 * (i + r))
    return world


def crossover_mark(x):
    return VGroup(
        Line([x - 0.22, 0.5, 0], [x + 0.22, -0.5, 0], color=RED, stroke_width=8),
        Line([x + 0.22, 0.5, 0], [x - 0.22, -0.5, 0], color=RED, stroke_width=8),
    )


def switch_arc(x, direction=1):
    """Two honest schematic paths showing homologous tails exchanging."""
    a = CurvedArrow([x - 0.4, RIBBON_Y[0] - 0.35, 0], [x + 0.45, RIBBON_Y[1] + 0.35, 0],
                    angle=-0.65 * direction, color=RED, stroke_width=5, tip_length=0.16)
    b = CurvedArrow([x + 0.4, RIBBON_Y[1] + 0.35, 0], [x - 0.45, RIBBON_Y[0] - 0.35, 0],
                    angle=-0.65 * direction, color=RED, stroke_width=5, tip_length=0.16)
    return VGroup(a, b)


def pattern_card(pattern, border, at, title=None, order=(0, 1, 2), green_c=False, scale=1.0):
    """A broad A/B/C gamete card, always written in the requested slot order."""
    frame = RoundedRectangle(corner_radius=0.18, width=4.6 * scale, height=1.45 * scale,
                             stroke_color=border, stroke_width=4, fill_color=border, fill_opacity=0.09).move_to(at)
    xs = np.linspace(frame.get_left()[0] + 0.78 * scale, frame.get_right()[0] - 0.78 * scale, 3)
    chips = VGroup()
    for slot, idx in enumerate(order):
        letter, allele_color = pattern[idx]
        col = GREEN if green_c and letter == "C" else allele_color
        chips.add(marker_block(letter, col, xs[slot], at[1], middle=(letter == "C" and green_c),
                               fill=allele_color, scale=0.72 * scale))
    g = VGroup(frame, chips)
    if title:
        t = T(title, 26 * scale, border).next_to(frame, UP, buff=0.13)
        g.add(t)
    g.frame, g.chips = frame, chips
    return g


P_BLUE = (("A", BLUE), ("B", BLUE), ("C", BLUE))
P_GOLD = (("A", GOLD), ("B", GOLD), ("C", GOLD))
R_BLUE = (("A", BLUE), ("B", BLUE), ("C", GOLD))
R_GOLD = (("A", GOLD), ("B", GOLD), ("C", BLUE))


def four_pattern_cards(green_c=False, titles=True):
    """The exact prediction frame, shared by spoken, pause, and reveal scenes."""
    cards = VGroup(
        pattern_card(P_BLUE, BLUE, [-3.25, CARD_Y[0], 0], "parental?" if titles else None, green_c=green_c),
        pattern_card(P_GOLD, GOLD, [3.25, CARD_Y[0], 0], "parental?" if titles else None, green_c=green_c),
        pattern_card(R_BLUE, BLUE, [-3.25, CARD_Y[1], 0], "rare" if titles else None, green_c=green_c),
        pattern_card(R_GOLD, GOLD, [3.25, CARD_Y[1], 0], "rare" if titles else None, green_c=green_c),
    )
    return cards


def gene_map(y=0.2, labels=("A", "C", "B"), full=True):
    """The large carried A-C-B map."""
    xs = (-4.8, 0.0, 4.8)
    bands = VGroup(
        RoundedRectangle(corner_radius=0.18, width=4.25, height=1.1, stroke_opacity=0,
                         fill_color=BLUE, fill_opacity=0.24).move_to([-2.4, y, 0]),
        RoundedRectangle(corner_radius=0.18, width=4.25, height=1.1, stroke_opacity=0,
                         fill_color=GOLD, fill_opacity=0.24).move_to([2.4, y, 0]),
    )
    line = VGroup(
        bands,
        Line([xs[0] + 0.58, y, 0], [xs[1] - 0.58, y, 0], color=GREY, stroke_width=12),
        Line([xs[1] + 0.58, y, 0], [xs[2] - 0.58, y, 0], color=GREY, stroke_width=12),
    )
    dots = VGroup()
    for x, lab in zip(xs, labels):
        col = GREEN if lab == "C" else TEXT
        circ = Circle(radius=0.52, stroke_color=col, stroke_width=6, fill_color=BG, fill_opacity=1).move_to([x, y, 0])
        dots.add(VGroup(circ, M(lab, 34, col).move_to(circ)))
    g = VGroup(line, dots)
    if full:
        g.add(T("left interval", 30, BLUE).move_to([-2.4, y + 0.82, 0]),
              T("right interval", 30, GOLD).move_to([2.4, y + 0.82, 0]))
    g.line, g.dots = line, dots
    return g


def class_bars():
    """Eight schematic class bars; heights encode only the stated rank groups."""
    heights = (3.8, 3.6, 2.25, 2.05, 1.8, 1.65, 0.6, 0.48)
    xs = np.linspace(-5.7, 5.7, 8)
    bars = VGroup()
    for i, (x, h) in enumerate(zip(xs, heights)):
        col = BLUE if i == 0 else GOLD if i == 1 else TEXT if i < 6 else RED
        r = RoundedRectangle(corner_radius=0.08, width=1.15, height=h, stroke_color=col, stroke_width=4,
                             fill_color=col, fill_opacity=0.28)
        r.move_to([x, -2.15 + h / 2, 0])
        bars.add(r)
    return bars


def mini_gamete(color, middle_color, at):
    line = Line(LEFT * 1.25, RIGHT * 1.25, color=color, stroke_width=12).move_to(at).set_opacity(0.6)
    blocks = VGroup(*[
        RoundedRectangle(corner_radius=0.06, width=0.52, height=0.48, stroke_color=(GREEN if i == 1 else c),
                         stroke_width=3, fill_color=c, fill_opacity=0.75).move_to([at[0] + (i - 1) * 0.85, at[1], 0])
        for i, c in enumerate((color, middle_color, color))
    ])
    return VGroup(line, blocks)


class S00Hook(SpokenScene):
    def construct(self):
        world = chromosome_world(show_middle=True)
        self.play(FadeIn(world), run_time=1.0)
        self.at("outer markers looking untouched")
        x1, x2 = crossover_mark(-2.35), crossover_mark(2.35)
        a1, a2 = switch_arc(-2.35), switch_arc(2.35, -1)
        self.play(Create(x1), Create(a1), run_time=0.75)
        self.play(Create(x2), Create(a2), run_time=0.75)
        product = chromosome_world(show_middle=True, product=True)
        self.play(ReplacementTransform(world, product), FadeOut(a1), FadeOut(a2), run_time=0.9)
        bob(product, amp=0.10, speed=1.0)
        outer = VGroup(product[0][1][0], product[0][1][2])
        self.play(Indicate(outer, color=TEXT, scale_factor=1.08), run_time=0.7)
        self.at("How can offspring reveal")
        q = T("What reveals two switches?", 38, TEXT).move_to([0, 3.15, 0])
        self.play(FadeIn(q, shift=DOWN * 0.12), run_time=0.6)
        pulse(x1), pulse(x2)
        self.add(scope_tag("schematic"))
        self.finish()


class S01Title(TitleCard):
    LESSON = "Three-Point Crosses: Gene Order and Double Crossovers"
    TITLE = "The Marker in the Middle"

    def construct(self):
        world = chromosome_world(show_middle=True, product=True, drift=True).set_opacity(0.42)
        x1, x2 = crossover_mark(-2.35), crossover_mark(2.35)
        pulse(x1), pulse(x2)
        title = T(self.TITLE, 54, TEXT, font=TITLE_FONT).move_to([0, 3.08, 0])
        self.add(world, x1, x2)
        self.play(FadeIn(title, shift=UP * 0.12), run_time=0.65)
        self.finish()


class S02Switches(SpokenScene):
    def construct(self):
        world = chromosome_world(show_middle=True, labels=True)
        bob(world, amp=0.09, speed=0.9)
        breathe_ribbons(world)
        self.play(FadeIn(world[0], shift=RIGHT * 0.25), run_time=0.7)
        self.at("one gold chromosome")
        self.play(FadeIn(world[1], shift=LEFT * 0.25), run_time=0.7)
        self.at("three marker blocks")
        self.play(LaggedStart(*[Indicate(world[r][1], scale_factor=1.04) for r in (0, 1)], lag_ratio=0.25), run_time=0.9)
        self.play(FadeIn(world[2:]), run_time=0.4)
        n = ValueTracker(0)
        count = counter("switches  {:.0f}", n, at=[0, -3.15, 0], size=30, color=RED)
        self.add(count)
        self.at("A red crossover point")
        x1, arc1 = crossover_mark(-2.35), switch_arc(-2.35)
        self.play(Create(x1), Create(arc1), n.animate.set_value(1), run_time=1.0)
        self.at("One crossover changes")
        one = chromosome_world(show_middle=True, labels=True)
        one[0][1][2][0].set_fill(GOLD)
        one[1][1][2][0].set_fill(BLUE)
        bob(one, amp=0.09, speed=0.9)
        breathe_ribbons(one)
        self.play(ReplacementTransform(world, one), FadeOut(arc1), run_time=1.0)
        self.at("A second swap")
        x2, arc2 = crossover_mark(2.35), switch_arc(2.35, -1)
        self.play(Create(x2), Create(arc2), n.animate.set_value(2), run_time=1.0)
        restored = chromosome_world(show_middle=True, product=True, labels=True)
        bob(restored, amp=0.09, speed=0.9)
        breathe_ribbons(restored)
        self.play(ReplacementTransform(one, restored), FadeOut(arc2), run_time=1.0)
        self.play(Indicate(VGroup(restored[0][1][0], restored[0][1][2]), color=BLUE), run_time=0.7)
        self.finish()


class S03Middle(SpokenScene):
    def construct(self):
        base = chromosome_world(show_middle=False)
        bob(base, amp=0.09, speed=0.9)
        self.add(base)
        middle = VGroup(base[0][1][1], base[1][1][1]).set_opacity(1)
        self.at("place a green marker")
        self.play(FadeIn(middle, scale=0.5), run_time=0.9)
        self.at("After two swaps")
        x1, x2 = crossover_mark(-2.35), crossover_mark(2.35)
        self.play(Create(x1), Create(switch_arc(-2.35)), run_time=0.8)
        self.play(Create(x2), Create(switch_arc(2.35, -1)), run_time=0.8)
        product = chromosome_world(show_middle=True, product=True)
        bob(product, amp=0.09, speed=0.9)
        self.play(ReplacementTransform(base, product), run_time=1.0)
        self.at("outer colors again match")
        self.play(Indicate(VGroup(product[0][1][0], product[0][1][2]), color=BLUE), run_time=0.7)
        self.at("green middle marker does not")
        self.play(Indicate(product[0][1][1], color=GREEN, scale_factor=1.22), run_time=0.9)
        bracket = BraceBetweenPoints([-2.35, -2.35, 0], [2.35, -2.35, 0], direction=DOWN, color=RED)
        lab = T("hidden double crossover", 30, RED).next_to(bracket, DOWN, buff=0.15)
        self.at("hidden double crossover")
        self.play(Create(bracket), FadeIn(lab, shift=UP * 0.1), run_time=0.8)
        self.finish()


class S04TwoViews(SpokenScene):
    def construct(self):
        product = chromosome_world(show_middle=True, product=True, drift=False)
        template = ribbon_row(2.45, BLUE, show_middle=False).set_opacity(0.45)
        bob(product, amp=0.10, speed=1.0)
        bob(template, amp=0.07, speed=1.0, seed=2)
        self.add(product, template)
        shutter = RoundedRectangle(corner_radius=0.12, width=1.05, height=3.0, stroke_opacity=0,
                                   fill_color=BG, fill_opacity=0.98).move_to([0, 0, 0])
        shutter.layout_ok = "covered"  # deliberate occluder over the middle marker
        shutter_lab = T("outer markers only", 28, TEXT).move_to([0, 3.42, 0])
        shutter_group = VGroup(shutter, shutter_lab)
        self.at("Cover the middle marker")
        self.play(FadeIn(shutter_group, shift=DOWN * 0.2), run_time=0.9)
        self.at("looks parental")
        self.play(Indicate(VGroup(product[0][1][0], product[0][1][2], template), color=BLUE), run_time=0.9)
        self.at("Uncover it")
        self.play(FadeOut(shutter_group, shift=UP * 0.2), run_time=0.8)
        self.play(Indicate(product[0][1][1], color=GREEN, scale_factor=1.2), run_time=0.8)
        self.at("chromosome did not change")
        still = T("same chromosome", 30, TEXT).move_to([0, -3.0, 0])
        self.play(FadeIn(still), run_time=0.5)
        self.at("third observation changed")
        three = T("three markers", 30, GREEN).move_to(still)
        self.play(swap(still, three), run_time=0.7)
        self.finish()


class S05TestCross(SpokenScene):
    def construct(self):
        world = chromosome_world(show_middle=True, product=True).scale(0.47).move_to([-3.75, 1.35, 0])
        for row in world:
            for block in row[1]:
                block[1].set_opacity(0)
        bob(world, amp=0.09, speed=1.0)
        self.play(FadeIn(world), run_time=0.7)
        self.at("turns these chromosome patterns")
        arrow = Arrow([-2.15, 1.8, 0], [-0.7, 1.8, 0], color=TEXT, stroke_width=5, buff=0.05)
        self.play(GrowArrow(arrow), run_time=0.6)
        tester = VGroup(
            RoundedRectangle(corner_radius=0.16, width=4.2, height=1.35, stroke_color=GREY, stroke_width=3,
                             fill_color=GREY, fill_opacity=0.12),
            T("recessive tester", 28, GREY),
            VGroup(*[chip("a", GREY, 24), chip("b", GREY, 24), chip("c", GREY, 24)]).arrange(RIGHT, buff=0.22),
        )
        tester[1].move_to([3.5, 1.25, 0]); tester[2].move_to([3.5, 0.65, 0]); tester[0].move_to([3.5, 0.95, 0])
        pulse(tester[0], base=3, amp=1.2, speed=1.5)
        self.at("recessive tester contributes")
        self.play(FadeIn(tester), run_time=0.8)
        boxes = VGroup(*[
            RoundedRectangle(corner_radius=0.12, width=2.3, height=1.2, stroke_color=TEXT, stroke_width=3)
            for _ in range(3)
        ]).arrange(RIGHT, buff=0.45).move_to([0.8, -1.65, 0])
        self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.22), run_time=0.8)
        greys = VGroup(*[mini_gamete(GREY, GREY, b.get_center() + UP * 0.18).scale(0.62) for b in boxes])
        gametes = VGroup(mini_gamete(BLUE, GOLD, boxes[0].get_center() + DOWN * 0.2).scale(0.62),
                         mini_gamete(GOLD, BLUE, boxes[1].get_center() + DOWN * 0.2).scale(0.62),
                         mini_gamete(BLUE, BLUE, boxes[2].get_center() + DOWN * 0.2).scale(0.62))
        self.at("same alleles every time")
        self.play(LaggedStart(*[FadeIn(g) for g in greys], lag_ratio=0.2), run_time=0.8)
        self.at("each offspring phenotype reports")
        self.play(LaggedStart(*[FadeIn(g, shift=DOWN * 0.15) for g in gametes], lag_ratio=0.2), run_time=0.9)
        cards = VGroup(*[pattern_card(p, c, b.get_center(), scale=0.48) for p, c, b in
                         ((R_BLUE, BLUE, boxes[0]), (R_GOLD, GOLD, boxes[1]), (P_BLUE, BLUE, boxes[2]))])
        self.play(ReplacementTransform(VGroup(boxes, greys, gametes), cards), run_time=0.9)
        for i, c in enumerate(cards):
            bob(c, amp=0.07, speed=0.9, seed=i)
        self.finish()


class S06Classes(SpokenScene):
    def construct(self):
        cards = VGroup(*[
            RoundedRectangle(corner_radius=0.12, width=1.15, height=0.85,
                             stroke_color=BLUE if i % 2 == 0 else GOLD, stroke_width=4,
                             fill_color=BLUE if i % 2 == 0 else GOLD, fill_opacity=0.22)
            .move_to([-5.6 + i * 1.6, 0, 0])
            for i in range(8)
        ])
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.08), run_time=0.9)
        self.at("become eight bars")
        bars = class_bars()
        self.play(ReplacementTransform(cards, bars), run_time=1.2)
        for i, bar in enumerate(bars):
            pulse(bar, base=4, amp=1.1, speed=1.2 + 0.08 * i)
        base = Line([-6.3, -2.15, 0], [6.3, -2.15, 0], color=GREY, stroke_width=3)
        self.add(base, scope_tag("schematic"))
        self.at("largest pair")
        p = T("parental?", 30, TEXT).move_to([-4.9, 2.9, 0])
        self.play(FadeIn(p), Indicate(VGroup(bars[0], bars[1]), scale_factor=1.04), run_time=0.8)
        self.at("Two middle pairs")
        s = T("single crossovers", 30, TEXT).move_to([0.0, 1.35, 0])
        self.play(FadeIn(s), Indicate(VGroup(*bars[2:6]), color=TEXT), run_time=0.8)
        self.at("smallest pair")
        d = T("double crossovers?", 30, RED).move_to([4.55, -0.15, 0])
        self.play(FadeIn(d), Indicate(VGroup(bars[6], bars[7]), color=RED, scale_factor=1.15), run_time=0.8)
        self.at("Rarity is a clue")
        clue = caption("Rarity is a clue, not proof.", color=GOLD)
        self.play(FadeIn(clue), run_time=0.6)
        self.finish()


class S07Predict(SpokenScene):
    def construct(self):
        cards = four_pattern_cards()
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cards], lag_ratio=0.15), run_time=1.0)
        for i, c in enumerate(cards):
            bob(c, amp=0.065, speed=0.85, seed=i)
        self.add(scope_tag("schematic"))
        self.at("Which marker must")
        q = question_card("Which marker is in the middle?", y=3.25, size=36, max_w=9.5)
        self.play(FadeIn(q.question, shift=DOWN * 0.1), run_time=0.6)
        self.at("Compare each rare pattern")
        self.play(Indicate(VGroup(cards[0], cards[2]), color=BLUE, scale_factor=1.025), run_time=0.7)
        self.play(Indicate(VGroup(cards[1], cards[3]), color=GOLD, scale_factor=1.025), run_time=0.7)
        self.finish()


class S08PredictPause(PredictPause):
    QUESTION = "Which marker is in the middle?"
    SECONDS = 4.5
    CARD = {"y": 3.25, "size": 36, "max_w": 9.5}
    RING_AT = (4.2, -3.1, 0)

    def backdrop(self):
        cards = four_pattern_cards()
        for i, c in enumerate(cards):
            bob(c, amp=0.065, speed=0.85, seed=i)
            pulse(c.frame, base=4, amp=0.7, speed=1.2)
        return VGroup(cards, scope_tag("schematic"))


class S09Reveal(SpokenScene):
    def construct(self):
        cards = four_pattern_cards()
        q = question_card("Which marker is in the middle?", y=3.25, size=36, max_w=9.5)
        self.add(cards, q.question)
        self.at("Only marker C differs")
        green = four_pattern_cards(green_c=True)
        self.play(ReplacementTransform(cards, green), run_time=0.9)
        cs = VGroup(*[c.chips[2] for c in green])
        self.play(Indicate(cs, color=GREEN, scale_factor=1.12), run_time=0.8)
        self.at("C belongs in the middle")
        amap = gene_map(y=-0.15)
        self.play(FadeOut(green), FadeOut(q.question), FadeIn(amap, shift=UP * 0.15), run_time=1.0)
        bob(amap, amp=0.085, speed=0.9)
        self.at("written last")
        order = M("written A-B-C  →  map A-C-B", 34, TEXT).move_to([0, 2.3, 0])
        self.play(FadeIn(order), run_time=0.6)
        self.at("changed marker decided")
        self.play(Indicate(amap.dots[1], color=GREEN, scale_factor=1.18), run_time=0.8)
        edge_notes = VGroup(T("parental?", 24, TEXT).move_to([-5.75, -2.85, 0]),
                            T("double crossovers?", 24, RED).move_to([4.65, -2.85, 0]))
        self.play(FadeIn(edge_notes), run_time=0.4)
        self.at("Unequal survival")
        survival = ValueTracker(0.7)
        gauge = dial(survival, center=[4.85, 1.9, 0], radius=0.9, label="survival?", color=GREY,
                     fmt="{:.0f}%", size=28)
        self.play(FadeIn(gauge), survival.animate.set_value(0.35), run_time=1.0)
        self.finish()


def eight_small_cards(order=(0, 1, 2)):
    patterns = (P_BLUE, P_GOLD, R_BLUE, R_GOLD,
                (("A", BLUE), ("B", GOLD), ("C", BLUE)),
                (("A", GOLD), ("B", BLUE), ("C", GOLD)),
                (("A", BLUE), ("B", GOLD), ("C", GOLD)),
                (("A", GOLD), ("B", BLUE), ("C", BLUE)))
    cards = VGroup()
    for i, pat in enumerate(patterns):
        x = -4.9 + (i % 4) * 3.25
        y = 2.15 if i < 4 else 0.7
        cards.add(pattern_card(pat, BLUE if i % 2 == 0 else GOLD, [x, y, 0], order=order,
                               green_c=True, scale=0.55))
    return cards


class S10Reorder(SpokenScene):
    def construct(self):
        written = eight_small_cards((0, 1, 2))
        self.add(written, scope_tag("schematic"))
        self.at("Move the changed marker")
        mapped = eight_small_cards((0, 2, 1))
        self.play(ReplacementTransform(written, mapped, path_arc=0.35), run_time=1.2)
        for i, c in enumerate(mapped):
            bob(c, amp=0.075, speed=0.8, seed=i)
        m = gene_map(y=-2.15)
        self.play(FadeIn(m), run_time=0.7)
        pulse(m.line[1], base=12, amp=2.5, speed=1.5)
        pulse(m.line[2], base=12, amp=2.5, speed=1.7)
        self.at("single crossover pattern")
        left_beads = VGroup(*[Dot(radius=0.11, color=RED).move_to(mapped[i].get_bottom()) for i in (4, 5)])
        self.add(left_beads)
        self.play(*[b.animate.move_to([-2.4, -2.15, 0]) for b in left_beads], run_time=0.9)
        self.at("one interval")
        self.play(Indicate(m[2], color=BLUE), run_time=0.6)
        self.at("Each double changes")
        doubles = VGroup(*[Dot(radius=0.12, color=RED).move_to(mapped[i].get_bottom()) for i in (6, 7)])
        self.add(doubles)
        self.play(doubles[0].animate.move_to([-2.4, -2.15, 0]),
                  doubles[1].animate.move_to([2.4, -2.15, 0]), run_time=0.9)
        self.at("class list has become")
        self.play(Indicate(m, color=GREEN, scale_factor=1.03), run_time=0.8)
        self.finish()


class S11Distance(SpokenScene):
    def construct(self):
        m = gene_map(y=2.25)
        bob(m, amp=0.08, speed=0.85)
        pulse(m.line[1], base=12, amp=4.0, speed=1.7)
        pulse(m.line[2], base=12, amp=4.0, speed=1.9)
        self.add(m)
        left = Ledger([("singles", "one interval", BLUE), ("doubles", "also here", RED)],
                      top_left=(-5.9, 0.9), title="A–C ledger", width=5.2, key_w=2.0, row_h=0.75, size=26)
        right = Ledger([("singles", "one interval", GOLD), ("doubles", "also here", RED)],
                       top_left=(0.7, 0.9), title="C–B ledger", width=5.2, key_w=2.0, row_h=0.75, size=26)
        self.at("Count each single crossover")
        self.play(FadeIn(left), FadeIn(right), run_time=0.7)
        self.play(left.reveal(0), right.reveal(0), run_time=0.7)
        self.at("Count every double crossover")
        double = Dot(radius=0.22, color=RED).move_to([0, 1.55, 0])
        self.play(FadeIn(double), run_time=0.35)
        d1, d2 = double.copy(), double.copy()
        self.play(ReplacementTransform(double, VGroup(d1, d2)),
                  d1.animate.move_to([-1.3, -0.75, 0]), d2.animate.move_to([5.2, -0.75, 0]), run_time=0.9)
        bob(d1, amp=0.18, speed=1.45)
        bob(d2, amp=0.18, speed=1.65, seed=2)
        self.play(left.reveal(1), right.reveal(1), run_time=0.6)
        self.at("because each double crossed both")
        self.play(Indicate(VGroup(m[2], m[3]), color=RED), run_time=0.7)
        formula = M("cM = 100 × (singles + doubles) / total", 28, TEXT).move_to([0, -1.35, 0])
        self.at("Divide each interval count")
        self.play(FadeIn(formula, shift=UP * 0.1), run_time=0.7)
        self.at("express it in centimorgans")
        self.play(Indicate(formula, color=GREEN, scale_factor=1.04), run_time=0.7)
        bars = VGroup(Rectangle(width=4.1, height=0.5, stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.45),
                      Rectangle(width=5.2, height=0.5, stroke_color=GOLD, fill_color=GOLD, fill_opacity=0.45))
        bars.arrange(RIGHT, buff=0).move_to([0, -2.6, 0])
        self.at("adjacent distances then add")
        self.play(GrowFromEdge(bars[0], LEFT), GrowFromEdge(bars[1], LEFT), run_time=1.0)
        self.finish()


class S12BlindSpot(SpokenScene):
    def construct(self):
        m = gene_map(y=1.5)
        bob(m, amp=0.08, speed=0.85)
        full = VGroup(Rectangle(width=4.1, height=0.72, stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.45),
                      Rectangle(width=5.2, height=0.72, stroke_color=GOLD, fill_color=GOLD, fill_opacity=0.45))
        full.arrange(RIGHT, buff=0).move_to([0, -1.45, 0])
        counters = VGroup(Dot(radius=0.2, color=RED).move_to([-2.4, -1.45, 0]),
                          Dot(radius=0.2, color=RED).move_to([2.4, -1.45, 0]))
        self.add(m, full, counters, scope_tag("schematic distance"))
        self.at("Hide the green marker")
        shutter = RoundedRectangle(corner_radius=0.15, width=1.65, height=4.5, stroke_color=GREY, stroke_width=3,
                                   fill_color=BG, fill_opacity=0.98).move_to([0, 0.35, 0])
        shutter.layout_ok = "covered"  # deliberate occluder: hiding the middle marker is the narrated action
        self.play(FadeIn(shutter), run_time=0.8)
        self.at("Both swaps restore")
        self.play(counters.animate.move_to([0, -1.45, 0]).set_opacity(0), run_time=0.8)
        self.at("vanish from a two point count")
        short = Rectangle(width=7.0, height=0.72, stroke_color=GREY, fill_color=GREY, fill_opacity=0.35).move_to([-1.15, -1.45, 0])
        self.play(ReplacementTransform(full, short), run_time=0.9)
        tag = T("too short", 32, RED).move_to([0, -2.25, 0])
        self.at("map becomes too short")
        self.play(FadeIn(tag), run_time=0.5)
        self.at("middle marker is the witness")
        restored = VGroup(Rectangle(width=4.1, height=0.72, stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.45),
                          Rectangle(width=5.2, height=0.72, stroke_color=GOLD, fill_color=GOLD, fill_opacity=0.45))
        restored.arrange(RIGHT, buff=0).move_to([0, -1.45, 0])
        newc = VGroup(Dot(radius=0.2, color=RED).move_to([-2.4, -1.45, 0]),
                      Dot(radius=0.2, color=RED).move_to([2.4, -1.45, 0]))
        self.play(FadeOut(shutter), ReplacementTransform(short, restored), FadeIn(newc), FadeOut(tag), run_time=1.0)
        self.play(Indicate(m.dots[1], color=GREEN, scale_factor=1.2), run_time=0.7)
        self.finish()


class S13Scope(SpokenScene):
    def construct(self):
        world = chromosome_world(show_middle=True, product=True, drift=False).scale(0.45).move_to([3.3, 0.55, 0])
        for row in world:
            for block in row[1]:
                block[1].set_opacity(0)
        bob(world, amp=0.045, speed=0.65)
        self.add(world)
        checklist = Ledger([("✓", "scorable classes", GREEN),
                            ("✓", "short intervals", GREEN),
                            ("✓", "rare pair reciprocal and viable", GREEN)],
                           top_left=(-6.25, 2.2), title="works when", width=5.4, key_w=0.7,
                           row_h=0.82, size=25)
        self.at("classes are scoreable")
        self.play(FadeIn(checklist), checklist.reveal(0), run_time=0.8)
        self.at("adjacent intervals are short")
        self.play(checklist.reveal(1), run_time=0.65)
        self.at("Long intervals can hide more")
        caution = T("long intervals hide more", 28, RED).move_to([-3.8, -1.25, 0])
        self.play(FadeIn(caution), run_time=0.6)
        self.at("Rarity is a clue")
        clue = T("rarity ≠ proof", 30, GOLD).move_to([-3.8, -1.95, 0])
        self.play(FadeIn(clue), run_time=0.6)
        self.at("rare classes survive")
        self.play(checklist.reveal(2), run_time=0.8)
        self.at("middle marker makes")
        x1, x2 = crossover_mark(2.25).scale(0.45).move_to([2.25, 0.55, 0]), crossover_mark(4.35).scale(0.45).move_to([4.35, 0.55, 0])
        self.play(Create(x1), Create(x2), run_time=0.7)
        self.play(Indicate(VGroup(world[0][1][1], world[1][1][1]), color=GREEN, scale_factor=1.2), run_time=0.9)
        pulse(x1), pulse(x2)
        self.finish()


class S14End(EndCard):
    LINE = "A middle marker makes double crossovers visible."
