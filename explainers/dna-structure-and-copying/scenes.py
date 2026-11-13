from bp_parts import *


# COLOR MAP: old strand/backbone GREY; new strand GOLD; A RED; T BLUE;
# C GREEN; G PURPLE; labels TEXT. These colours never change meaning.
PURPLE = "#B58AE8"
BASE_COLOR = {"A": RED, "T": BLUE, "C": GREEN, "G": PURPLE}
PAIR = {"A": "T", "T": "A", "C": "G", "G": "C"}
SEQ = "GATTCA"
PARTNER = "CTAAGT"


class FilmSpokenScene(SpokenScene):
    """A dense, gently breathing stage shared by every spoken scene."""

    def setup(self):
        super().setup()
        self.stage = RoundedRectangle(corner_radius=0.28, width=12.8, height=6.8,
                                      stroke_color="#405371", stroke_width=2,
                                      fill_color="#263653", fill_opacity=1).set_z_index(-20)
        self.stage.layout_ok = True  # deliberate full-scene backdrop behind all labels
        self.add(self.stage)

    def wait(self, duration=1, *args, **kwargs):
        # Keep the actual diagram moving during narration gaps: a repeated, slow
        # horizontal breath is visible but returns every object to its exact place.
        if duration > 0.18 and self.mobjects:
            cycles = max(1, int(np.ceil(duration / 1.2)))
            dt = duration / cycles
            for _ in range(cycles):
                movers = [m for m in self.mobjects if m is not None]
                self.play(*[m.animate.shift(RIGHT * 0.18) for m in movers],
                          rate_func=there_and_back, run_time=dt)
        else:
            super().wait(duration, *args, **kwargs)


def p(x, y):
    return np.array([x, y, 0.0])


def base_block(letter, width=1.0, height=0.58, font_size=32, dashed=False):
    col = BASE_COLOR[letter]
    box_cls = DashedVMobject if dashed else None
    box = RoundedRectangle(corner_radius=0.1, width=width, height=height,
                           stroke_color=col, stroke_width=3,
                           fill_color=col, fill_opacity=0.32)
    if box_cls:
        box = DashedVMobject(box, num_dashes=18)
    lab = T(letter, font_size, TEXT, weight=BOLD).move_to(box)
    lab.layout_ok = True  # letter deliberately sits inside its coloured base block
    return VGroup(box, lab)


def empty_slot(width=1.0, height=0.58):
    return DashedVMobject(RoundedRectangle(corner_radius=0.1, width=width, height=height,
                                           stroke_color=GREY, stroke_width=3), num_dashes=18)


def arrow_tip(point, direction, color=GREY, size=0.22):
    tip = Triangle(color=color, fill_color=color, fill_opacity=1, stroke_width=0).scale(size)
    if np.allclose(direction, DOWN):
        tip.rotate(PI)
    elif np.allclose(direction, LEFT):
        tip.rotate(PI / 2)
    elif np.allclose(direction, RIGHT):
        tip.rotate(-PI / 2)
    return tip.move_to(point)


def vertical_strand(seq, x=-1.65, bases_right=True, color=GREY, y_top=2.45,
                    spacing=0.86, block_w=1.05, arrow=True):
    ys = [y_top - i * spacing for i in range(len(seq))]
    base_x = x + (0.72 if bases_right else -0.72)
    backbone = Line(p(x, ys[0] + 0.38), p(x, ys[-1] - 0.38), color=color, stroke_width=12)
    ticks, blocks = VGroup(), VGroup()
    for ch, y in zip(seq, ys):
        tick = Line(p(x, y), p(base_x - (0.52 if bases_right else -0.52), y),
                    color=color, stroke_width=7)
        ticks.add(tick)
        blocks.add(base_block(ch, width=block_w).move_to(p(base_x, y)))
    parts = [backbone, ticks, blocks]
    if arrow:
        if bases_right:
            parts.append(arrow_tip(p(x, ys[-1] - 0.58), DOWN, color))
        else:
            parts.append(arrow_tip(p(x, ys[0] + 0.58), UP, color))
    g = VGroup(*parts)
    g.backbone, g.ticks, g.blocks = backbone, ticks, blocks
    g.arrow = parts[-1] if arrow else VGroup()
    return g


def vertical_ladder(seq=SEQ, partner=PARTNER, left_x=-1.65, right_x=1.65,
                    left_color=GREY, right_color=GREY, y_top=2.45, spacing=0.86):
    left = vertical_strand(seq, left_x, True, left_color, y_top, spacing)
    right = vertical_strand(partner, right_x, False, right_color, y_top, spacing)
    bonds = VGroup(*[
        DashedLine(a.get_right(), b.get_left(), dash_length=0.1, color=TEXT, stroke_width=3)
        for a, b in zip(left.blocks, right.blocks)
    ])
    g = VGroup(left, right, bonds)
    g.left, g.right, g.bonds = left, right, bonds
    return g


def horizontal_ladder(seq="ATCGTA", center=p(0, 0.25), scale=1.0):
    xs = np.linspace(-4.0, 4.0, len(seq))
    top_y, bot_y = 1.15, -0.65
    top = Line(p(xs[0] - 0.45, top_y), p(xs[-1] + 0.45, top_y), color=GREY, stroke_width=11)
    bot = Line(p(xs[0] - 0.45, bot_y), p(xs[-1] + 0.45, bot_y), color=GREY, stroke_width=11)
    tops, bots, bonds = VGroup(), VGroup(), VGroup()
    for x, ch in zip(xs, seq):
        a = base_block(ch, width=1.05, height=0.58, font_size=30).move_to(p(x, 0.68))
        b = base_block(PAIR[ch], width=1.05, height=0.58, font_size=30).move_to(p(x, -0.18))
        tops.add(a); bots.add(b)
        bonds.add(DashedLine(a.get_bottom(), b.get_top(), dash_length=0.08, color=TEXT, stroke_width=3))
    g = VGroup(top, bot, tops, bots, bonds).move_to(center).scale(scale)
    g.top_line, g.bot_line, g.top_blocks, g.bot_blocks, g.bonds = top, bot, tops, bots, bonds
    g.top_half = VGroup(top, tops)
    g.bot_half = VGroup(bot, bots)
    return g


def predict_world(with_slots=True):
    strand = vertical_strand(SEQ, x=-1.6, bases_right=True, y_top=2.45, spacing=0.86)
    slots = VGroup(*[empty_slot().move_to(p(1.6, 2.45 - i * 0.86)) for i in range(6)])
    pencil = VGroup(
        Rectangle(width=0.25, height=1.0, color=GOLD, fill_color=GOLD, fill_opacity=0.75),
        Triangle(color=TEXT, fill_color=TEXT, fill_opacity=1, stroke_width=0).scale(0.14).next_to(p(0, -0.5), DOWN, buff=0)
    ).rotate(-0.35).move_to(p(3.25, -0.1))
    return VGroup(strand, slots, pencil)


def template_world():
    left = vertical_strand(SEQ, x=-3.7, bases_right=True, y_top=2.45, spacing=0.7, block_w=0.82)
    right = vertical_strand(PARTNER, x=3.7, bases_right=False, y_top=2.45, spacing=0.7, block_w=0.82)
    return VGroup(left, right)


def small_molecule(seq, partner, cx, old_on_left=True):
    lx, rx = cx - 0.82, cx + 0.82
    lc, rc = (GREY, GOLD) if old_on_left else (GOLD, GREY)
    return vertical_ladder(seq, partner, lx, rx, lc, rc, y_top=1.8, spacing=0.62)


class S00Title(TitleCard):
    LESSON = "DNA: Structure and Copying"
    TITLE = "One Strand Is Enough"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", 20, TEAL, weight=BOLD).set_opacity(0.9)
        brand.layout_ok = True
        lesson = T(self.LESSON.upper(), 22, GREY)
        title = T(self.TITLE, 52, font=TITLE_FONT)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        ladder = horizontal_ladder("ATCG", center=p(0, -2.1), scale=0.55).set_opacity(0.65)
        heading = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.27).shift(UP * 0.65)
        self.play(FadeIn(brand), FadeIn(lesson), Write(title), GrowFromCenter(rule), run_time=1.0)
        self.play(FadeIn(ladder), Rotate(ladder, 0.09), run_time=1.0)
        self.play(Rotate(ladder, -0.18), rate_func=there_and_back, run_time=0.75)
        self.finish()


class S01Question(FilmSpokenScene):
    def construct(self):
        lad = horizontal_ladder()
        hands = VGroup(T("✋", 62, TEXT), T("✋", 62, TEXT)).arrange(RIGHT, buff=3.6).move_to(p(0, 0.25))
        self.at("Suppose I tore")
        self.play(FadeIn(lad), run_time=1.0)
        self.at("down the middle")
        self.play(FadeIn(hands), hands.animate.shift(RIGHT * 0.05), run_time=0.75)
        self.at("threw one half away")
        bin_box = VGroup(Rectangle(width=2.0, height=1.4, color=GREY, fill_color=GREY, fill_opacity=0.12),
                         T("BIN", 30, GREY)).move_to(p(0, -2.65))
        bin_box[1].move_to(bin_box[0]); bin_box[1].layout_ok = True
        self.play(FadeIn(bin_box), FadeOut(hands), lad.bot_half.animate.shift(DOWN * 3.6),
                  FadeOut(lad.bonds), run_time=1.5)
        self.remove(lad.bot_half)
        self.at("Could you rebuild")
        q = T("?", 92, GOLD, weight=BOLD).move_to(p(0, -0.9))
        self.play(FadeIn(q, scale=0.5), run_time=0.8)
        pulse(q, base=5, amp=2, speed=3)
        self.at("letter for letter")
        slots = VGroup(*[empty_slot().move_to(b.get_center() + DOWN * 0.86) for b in lad.top_blocks])
        self.play(LaggedStart(*[Create(s) for s in slots], lag_ratio=0.12), FadeOut(bin_box), run_time=1.1)
        self.at("By the end")
        check = T("YOU CAN", 38, GREEN, weight=BOLD).move_to(p(0, -2.55))
        self.play(FadeOut(q), FadeIn(check, shift=UP * 0.2), run_time=0.75)
        self.finish()


class S02Nucleotide(FilmSpokenScene):
    def construct(self):
        sugar = chip("sugar", GREY, 30).move_to(p(-2.25, 0.25))
        phosphate = VGroup(Circle(radius=0.58, color=TEAL, fill_color=TEAL, fill_opacity=0.2),
                           T("phosphate", 24, TEAL)).move_to(p(0, 1.55))
        phosphate[1].layout_ok = True
        base = chip("base", RED, 32).move_to(p(2.25, 0.25))
        self.at("Start with one")
        self.play(FadeIn(sugar, shift=LEFT * 0.4), run_time=0.7)
        self.at("a nucleotide")
        self.play(FadeIn(phosphate, shift=UP * 0.3), FadeIn(base, shift=RIGHT * 0.4), run_time=0.8)
        links = VGroup(Line(sugar.get_right(), base.get_left(), color=TEXT, stroke_width=5),
                       Line(phosphate.get_bottom(), sugar.get_top(), color=TEXT, stroke_width=5))
        self.play(Create(links), run_time=0.6)
        label = T("NUCLEOTIDE", 34, GOLD, weight=BOLD).move_to(p(0, 3.15))
        self.play(FadeIn(label), run_time=0.5)
        self.at("It has three parts")
        self.play(LaggedStart(Indicate(sugar), Indicate(phosphate), Indicate(base), lag_ratio=0.2), run_time=1.0)
        self.at("sugar called deoxyribose")
        sugar2 = chip("sugar\n(deoxyribose)", GREY, 26).move_to(sugar)
        links2 = VGroup(Line(sugar2.get_right(), base.get_left(), color=TEXT, stroke_width=5),
                        Line(phosphate.get_bottom(), sugar2.get_top(), color=TEXT, stroke_width=5))
        self.play(ReplacementTransform(sugar, sugar2), ReplacementTransform(links, links2), run_time=0.7)
        self.at("phosphate group")
        self.play(Indicate(phosphate, color=TEAL), run_time=0.55)
        self.at("and a base")
        self.play(Indicate(base, color=RED), run_time=0.55)
        self.at("base carries")
        info = T("information", 30, GOLD).next_to(base, DOWN, buff=0.35)
        self.play(FadeIn(info, shift=UP * 0.15), run_time=0.65)
        self.at("DNA uses four bases")
        self.play(FadeOut(VGroup(sugar2, phosphate, base, links2, info, label)), run_time=0.55)
        cards = VGroup()
        for ch, name in zip("ATCG", ["adenine", "thymine", "cytosine", "guanine"]):
            b = base_block(ch, 1.35, 0.9, 42)
            n = T(name, 27, BASE_COLOR[ch]).next_to(b, DOWN, buff=0.25)
            cards.add(VGroup(b, n))
        cards.arrange(RIGHT, buff=0.75).move_to(p(0, 0.1))
        for phrase, card in zip(["adenine", "thymine", "cytosine", "guanine"], cards):
            self.at(phrase)
            self.play(FadeIn(card, shift=UP * 0.3), run_time=0.45)
        self.at("We write them")
        self.play(LaggedStart(*[Indicate(c[0], color=BASE_COLOR[ch]) for c, ch in zip(cards, "ATCG")], lag_ratio=0.15), run_time=1.0)
        self.finish()


class S03Strand(FilmSpokenScene):
    def construct(self):
        loose = VGroup(*[base_block(ch).move_to(p(-0.7, 2.4 - i * 1.25)) for i, ch in enumerate("ATCG")])
        sugars = VGroup(*[chip("sugar", GREY, 24).move_to(p(-2.1, 2.4 - i * 1.25)) for i in range(4)])
        phosphates = VGroup(*[Circle(radius=0.22, color=TEAL, fill_color=TEAL, fill_opacity=0.35).move_to(p(-2.1, 1.78 - i * 1.25)) for i in range(3)])
        self.at("Nucleotides join")
        self.play(LaggedStart(*[FadeIn(VGroup(s, b), shift=RIGHT * 0.2) for s, b in zip(sugars, loose)], lag_ratio=0.12), run_time=1.2)
        self.at("called a strand")
        self.play(LaggedStart(*[FadeIn(q) for q in phosphates], lag_ratio=0.15), run_time=0.8)
        self.at("sugar of one")
        links = VGroup(*[Line(sugars[i].get_bottom(), phosphates[i].get_top(), color=TEXT, stroke_width=5) for i in range(3)],
                       *[Line(phosphates[i].get_bottom(), sugars[i + 1].get_top(), color=TEXT, stroke_width=5) for i in range(3)])
        self.play(LaggedStart(*[Create(x) for x in links], lag_ratio=0.12), run_time=1.2)
        self.at("That is a covalent bond")
        cov = T("covalent bond", 30, TEAL).move_to(p(2.4, 1.55))
        lead = Arrow(cov.get_left(), phosphates[0].get_right(), buff=0.12, color=TEAL)
        self.play(FadeIn(cov), GrowArrow(lead), run_time=0.7)
        self.at("a strong bond")
        strong = T("strong", 32, GOLD, weight=BOLD).move_to(p(2.4, 0.75))
        self.play(FadeIn(strong), Indicate(links, color=GOLD), run_time=0.8)
        self.at("share electrons")
        self.play(FadeOut(VGroup(cov, lead, strong)), run_time=0.45)
        self.at("bases stick out")
        strand = vertical_strand("ATCG", x=-1.9, bases_right=True, y_top=2.35, spacing=1.25)
        count = T("strands  1", 30, TEXT).move_to(p(4.7, 3.1))
        self.play(ReplacementTransform(VGroup(loose, sugars, phosphates, links), strand), FadeIn(count), run_time=1.2)
        self.play(LaggedStart(*[Indicate(b, color=BASE_COLOR[ch]) for b, ch in zip(strand.blocks, "ATCG")], lag_ratio=0.12), run_time=0.9)
        self.finish()


class S04Pairing(FilmSpokenScene):
    def construct(self):
        left = vertical_strand(SEQ, -1.65, True)
        right = vertical_strand(PARTNER, 5.0, False)
        self.add(left)
        self.at("second strand lines up")
        self.play(FadeIn(right), right.animate.move_to(vertical_strand(PARTNER, 1.65, False).get_center()), run_time=1.3)
        right.move_to(vertical_strand(PARTNER, 1.65, False).get_center())
        self.at("bases facing bases")
        self.play(LaggedStart(*[Indicate(VGroup(a, b), color=TEXT) for a, b in zip(left.blocks, right.blocks)], lag_ratio=0.08), run_time=1.0)
        self.at("Weak attractions called")
        bonds = VGroup(*[DashedLine(a.get_right(), b.get_left(), dash_length=0.1, color=TEXT, stroke_width=3)
                         for a, b in zip(left.blocks, right.blocks)])
        self.play(LaggedStart(*[Create(b) for b in bonds], lag_ratio=0.1), run_time=1.1)
        self.at("hydrogen bonds")
        hlabel = T("hydrogen bonds", 29, TEXT).move_to(p(4.6, -2.6))
        leader = Arrow(hlabel.get_left(), bonds[-1].get_right(), buff=0.12, color=TEXT)
        self.play(FadeIn(hlabel), GrowArrow(leader), run_time=0.7)
        self.at("only two kinds")
        count = T("strands  2", 30, TEXT).move_to(p(4.7, 3.1))
        self.play(FadeOut(VGroup(hlabel, leader)), FadeIn(count), run_time=0.55)
        self.at("A fits with T")
        ats = [VGroup(left.blocks[i], right.blocks[i]) for i, ch in enumerate(SEQ) if ch in "AT"]
        self.play(*[Indicate(x, color=GOLD) for x in ats], run_time=0.85)
        self.at("C fits with G")
        cgs = [VGroup(left.blocks[i], right.blocks[i]) for i, ch in enumerate(SEQ) if ch in "CG"]
        self.play(*[Indicate(x, color=GOLD) for x in cgs], run_time=0.85)
        self.finish()


class S05Misfit(FilmSpokenScene):
    def construct(self):
        a = base_block("A", 2.0, 1.25, 52).move_to(p(-3.4, 0.7))
        c = base_block("C", 2.0, 1.25, 52).move_to(p(3.8, 0.7))
        self.at("Watch what happens")
        self.play(FadeIn(a), FadeIn(c), c.animate.shift(LEFT * 2.25), run_time=1.2)
        self.at("edges do not match")
        gap = DoubleArrow(p(-0.45, 0.7), p(0.45, 0.7), color=RED, stroke_width=5)
        self.play(Create(gap), Wiggle(c), run_time=0.8)
        self.at("fit badly")
        cross = T("×", 80, RED, weight=BOLD).move_to(p(0, -0.55))
        self.play(FadeIn(cross, scale=0.5), c.animate.shift(RIGHT * 2.25), FadeOut(gap), run_time=0.8)
        self.at("That is the base")
        rule = caption("BASE-PAIRING RULE", 32, GOLD)
        self.play(FadeIn(rule), run_time=0.6)
        self.at("A always pairs")
        t = base_block("T", 2.0, 1.25, 52).move_to(p(3.8, 0.7))
        self.play(FadeOut(c), FadeOut(cross), FadeIn(t), t.animate.shift(LEFT * 2.8), run_time=1.0)
        self.at("C always pairs")
        c2 = base_block("C", 1.55, 0.95, 44).move_to(p(-1.0, -1.65))
        g2 = base_block("G", 1.55, 0.95, 44).move_to(p(3.2, -1.65))
        self.play(FadeIn(c2), FadeIn(g2), g2.animate.shift(LEFT * 2.2), run_time=0.9)
        summary = T("A with T     C with G", 34, GOLD, weight=BOLD).move_to(p(0, -3.05))
        self.play(ReplacementTransform(rule, summary), run_time=0.55)
        self.finish()


class S06Helix(FilmSpokenScene):
    def construct(self):
        ladder = vertical_ladder()
        self.add(ladder)
        self.at("Notice the two arrowheads")
        self.play(Indicate(ladder.left.arrow, color=GOLD), Indicate(ladder.right.arrow, color=GOLD), run_time=1.0)
        self.at("Each strand has")
        dl = Arrow(p(-2.7, 1.1), p(-2.7, -1.1), color=GREY, stroke_width=6)
        ur = Arrow(p(2.7, -1.1), p(2.7, 1.1), color=GREY, stroke_width=6)
        self.play(GrowArrow(dl), GrowArrow(ur), run_time=0.8)
        self.at("opposite ways")
        self.play(Indicate(dl, color=GOLD), Indicate(ur, color=GOLD), run_time=0.75)
        self.at("ladder twists")
        ys = np.linspace(2.65, -2.65, 120)
        phase = np.linspace(0, 2.4 * PI, 120)
        x1, x2 = 1.65 * np.sin(phase), -1.65 * np.sin(phase)
        side1 = VMobject(color=GREY, stroke_width=10).set_points_as_corners([p(x, y) for x, y in zip(x1, ys)])
        side2 = VMobject(color=GREY, stroke_width=10).set_points_as_corners([p(x, y) for x, y in zip(x2, ys)])
        rungs = VGroup(*[Line(p(x1[i], ys[i]), p(x2[i], ys[i]), color=BASE_COLOR[SEQ[(i // 20) % 6]], stroke_width=7)
                         for i in range(5, 120, 11)])
        helix = VGroup(side1, side2, rungs)
        self.play(FadeOut(VGroup(dl, ur)), ReplacementTransform(ladder, helix), run_time=1.7)
        tag = scope_tag("schematic")
        self.add(tag)
        self.at("backbones are the sides")
        sides = T("backbones = sides", 30, GREY).move_to(p(-4.55, 2.9))
        self.play(FadeIn(sides), Indicate(VGroup(side1, side2), color=GOLD), run_time=0.8)
        self.at("base pairs are the rungs")
        rlab = T("base pairs = rungs", 30, TEXT).move_to(p(4.4, -2.35))
        self.play(FadeIn(rlab), Indicate(rungs, color=GOLD), run_time=0.8)
        flat = vertical_ladder()
        self.play(FadeOut(VGroup(sides, rlab, tag)), ReplacementTransform(helix, flat), run_time=1.0)
        self.finish()


class S07Predict(FilmSpokenScene):
    def construct(self):
        world = predict_world()
        strand, slots, pencil = world
        self.at("Here is one strand")
        self.play(FadeIn(strand, shift=LEFT * 0.3), run_time=0.9)
        self.at("It reads")
        self.play(LaggedStart(*[Indicate(b, color=BASE_COLOR[ch]) for b, ch in zip(strand.blocks, SEQ)], lag_ratio=0.12), run_time=1.25)
        self.at("Before I fill")
        self.play(LaggedStart(*[Create(s) for s in slots], lag_ratio=0.1), run_time=1.0)
        self.at("write the")
        self.play(FadeIn(pencil, shift=UP * 0.2), Rotate(pencil, 0.18), run_time=0.65)
        q = question_card("What is the partner strand?", y=-3.2, size=30)
        self.play(FadeIn(q), run_time=0.55)
        self.finish()


class S08Pause(PredictPause):
    QUESTION = "What is the partner strand?"
    CARD = {"y": -3.2, "size": 30}

    def backdrop(self):
        stage = RoundedRectangle(corner_radius=0.28, width=12.8, height=6.8,
                                 stroke_color="#405371", stroke_width=2,
                                 fill_color="#263653", fill_opacity=1).set_z_index(-20)
        stage.layout_ok = True  # deliberate full-scene backdrop behind all labels
        return VGroup(stage, predict_world())


class S09Reveal(FilmSpokenScene):
    def construct(self):
        world = predict_world()
        strand, slots, pencil = world
        self.add(world, question_card("What is the partner strand?", y=-3.2, size=30))
        filled = []
        self.at("across from G")
        c = base_block("C").move_to(slots[0]); filled.append(c)
        self.play(FadeOut(slots[0]), FadeIn(c, shift=RIGHT * 0.35), run_time=0.75)
        self.at("across from a")
        t = base_block("T").move_to(slots[1]); filled.append(t)
        self.play(FadeOut(slots[1]), FadeIn(t, shift=RIGHT * 0.35), run_time=0.75)
        self.at("partner reads")
        rest = []
        for i, ch in enumerate(PARTNER[2:], 2):
            b = base_block(ch).move_to(slots[i]); filled.append(b); rest.append(b)
        self.play(LaggedStart(*[AnimationGroup(FadeOut(slots[i]), FadeIn(b, shift=RIGHT * 0.3))
                                for i, b in enumerate(rest, 2)], lag_ratio=0.16), run_time=1.5)
        self.at("Not one letter")
        self.play(FadeOut(pencil), LaggedStart(*[Indicate(b, color=GOLD) for b in filled], lag_ratio=0.1), run_time=1.0)
        self.at("One strand fixed")
        pair = VGroup(strand, *filled)
        bracket = Brace(pair, RIGHT, color=GOLD)
        label = fit_text("one strand fixes its partner", 3.2, 30, GOLD, max_lines=2).next_to(bracket, RIGHT, buff=0.2)
        self.play(FadeOut(self.mobjects[-1]), GrowFromCenter(bracket), FadeIn(label), run_time=0.9)
        self.finish()


class S10Unzip(FilmSpokenScene):
    def construct(self):
        start = vertical_ladder(SEQ, PARTNER, -0.82, 0.82, y_top=2.45, spacing=0.7)
        self.at("here is how")
        self.play(FadeIn(start), run_time=0.8)
        self.at("Enzymes unzip")
        wedge = VGroup(Triangle(color=TEAL, fill_color=TEAL, fill_opacity=0.3).scale(0.55),
                       T("enzyme", 24, TEAL)).move_to(p(0, 2.8))
        wedge[1].layout_ok = True
        self.play(FadeIn(wedge), wedge.animate.move_to(p(0, -2.4)),
                  start.left.animate.move_to(template_world()[0].get_center()),
                  start.right.animate.move_to(template_world()[1].get_center()),
                  FadeOut(start.bonds), run_time=2.1)
        templates = template_world()
        self.remove(start, wedge)
        self.add(templates)
        self.at("each old strand")
        labs = VGroup(T("template", 30, GREY).move_to(p(-3.7, -2.3)),
                      T("template", 30, GREY).move_to(p(3.7, -2.3)))
        self.play(FadeIn(labs), run_time=0.65)
        self.at("A template is")
        definition = caption("template = a pattern", 31, GOLD)
        self.play(FadeIn(definition), run_time=0.6)
        self.at("sets the order")
        self.play(LaggedStart(*[Indicate(b, color=GOLD) for s in templates for b in s.blocks], lag_ratio=0.05), run_time=1.2)
        self.finish()


class S11Two(FilmSpokenScene):
    def construct(self):
        templates = template_world()
        left_old, right_old = templates
        self.add(templates)
        new_left = vertical_strand(PARTNER, -2.05, False, GOLD, 2.45, 0.7, 0.82)
        new_right = vertical_strand(SEQ, 2.05, True, GOLD, 2.45, 0.7, 0.82)
        self.at("New nucleotides line up")
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.3) for b in new_left.blocks],
                              *[FadeIn(b, shift=LEFT * 0.3) for b in new_right.blocks], lag_ratio=0.07), run_time=1.5)
        self.at("each one matching")
        self.play(LaggedStart(*[Indicate(VGroup(a, b), color=GOLD) for a, b in zip(left_old.blocks, new_left.blocks)],
                              *[Indicate(VGroup(a, b), color=GOLD) for a, b in zip(right_old.blocks, new_right.blocks)], lag_ratio=0.05), run_time=1.2)
        self.at("copying ends")
        self.play(Create(new_left.backbone), Create(new_left.ticks), Create(new_right.backbone), Create(new_right.ticks),
                  FadeIn(new_left.arrow), FadeIn(new_right.arrow), run_time=1.2)
        bonds = VGroup(*[DashedLine(a.get_right(), b.get_left(), color=TEXT, dash_length=0.08) for a, b in zip(left_old.blocks, new_left.blocks)],
                       *[DashedLine(a.get_left(), b.get_right(), color=TEXT, dash_length=0.08) for a, b in zip(right_old.blocks, new_right.blocks)])
        self.play(Create(bonds), run_time=0.55)
        self.at("two molecules")
        count = T("molecules  2", 34, TEXT, weight=BOLD).move_to(p(0, 3.25))
        self.play(FadeIn(count), run_time=0.55)
        self.at("one old gray")
        oldlabs = VGroup(T("old", 27, GREY).move_to(p(-5.2, 2.7)), T("old", 27, GREY).move_to(p(5.2, 2.7)))
        self.play(FadeIn(oldlabs), run_time=0.55)
        self.at("one new gold")
        newlabs = VGroup(T("new", 27, GOLD).move_to(p(-1.9, -2.7)), T("new", 27, GOLD).move_to(p(1.9, -2.7)))
        self.play(FadeIn(newlabs), run_time=0.55)
        self.at("same base order")
        check = T("✓  same base order", 32, GREEN, weight=BOLD).move_to(p(0, -3.25))
        self.play(FadeOut(VGroup(oldlabs, newlabs)), FadeIn(check),
                  LaggedStart(*[Indicate(b, color=GREEN) for b in left_old.blocks + right_old.blocks], lag_ratio=0.06), run_time=1.2)
        self.finish()


class S12Rule(FilmSpokenScene):
    def construct(self):
        m1 = small_molecule(SEQ, PARTNER, -3.5, True).scale(0.58).move_to(p(-3.6, 2.25))
        m2 = small_molecule(SEQ, PARTNER, 3.5, False).scale(0.58).move_to(p(3.6, 2.25))
        self.at("pairing tells")
        self.play(FadeIn(m1), FadeIn(m2), run_time=0.8)
        pairs = VGroup(base_block("A", 1.3, 0.8, 38), base_block("T", 1.3, 0.8, 38),
                       T("and", 30, TEXT), base_block("C", 1.3, 0.8, 38), base_block("G", 1.3, 0.8, 38))
        pairs.arrange(RIGHT, buff=0.28).move_to(p(0, 0.25))
        self.at("Because a pair")
        self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.2) for x in pairs], lag_ratio=0.1), run_time=1.1)
        self.at("each strand fixes")
        rule = T("EACH STRAND FIXES ITS PARTNER", 39, GOLD, weight=BOLD).move_to(p(0, -1.55))
        self.play(FadeIn(rule, shift=UP * 0.2), run_time=0.85)
        self.at("Pairing does not yet")
        self.play(FadeOut(pairs), m1.animate.scale(0.82), m2.animate.scale(0.82), run_time=0.6)
        accuracy = T("accuracy  ?", 34, GREY).move_to(p(0, -2.65))
        self.play(FadeIn(accuracy), run_time=0.65)
        self.at("almost every letter right")
        self.play(Wiggle(accuracy), FadeOut(accuracy), run_time=0.8)
        self.finish()


class S13End(EndCard):
    LINE = "Each strand fixes its partner, so either can restore the whole molecule."
