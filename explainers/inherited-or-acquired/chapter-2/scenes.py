"""Dominant Is Not Popular — chapter 2 of Inherited or Acquired?

COLOR MAP (shared with chapter 1's revised script)
  BLUE = genes and alleles
  GREEN = environment
  GOLD = acquired body changes
  TEAL = routes to offspring and the conceptual divider
  RED = stopped routes and rejected meanings
  GREY = people, recessive cards, bowls, and other structures

The population bowl and genotype display are rebuilt by the builder functions below so every
carried landmark stays at exactly the same scale and screen position.
"""
from bp_parts import *  # noqa: F401,F403
import numpy as np


BOWL_C = np.array([-3.65, 0.45, 0.0])
PAIR_C = np.array([3.55, 1.05, 0.0])
CARD_POS = [
    (-5.55, 1.45), (-4.75, 1.85), (-3.85, 1.55), (-2.85, 1.85), (-1.95, 1.25),
    (-5.75, 0.55), (-4.85, 0.75), (-3.95, 0.55), (-3.05, 0.75), (-2.15, 0.35),
    (-5.55, -0.35), (-4.65, -0.15), (-3.75, -0.45), (-2.85, -0.15), (-2.05, -0.55),
    (-5.05, -1.05), (-4.05, -1.20), (-3.05, -1.00), (-2.35, -1.25),
]
BLUE_IDS = {2, 10, 17}


def allele_card(color=GREY, width=0.52, height=0.34):
    """A plain allele card; labels are added only when narration names them."""
    return RoundedRectangle(
        corner_radius=0.07, width=width, height=height,
        stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.34,
    )


def person_outline(center, scale=1.0):
    c = np.array(center, dtype=float)
    if c.size == 2:
        c = np.append(c, 0.0)
    head = Circle(radius=0.18 * scale, color=GREY, stroke_width=3).move_to(c + UP * 0.34 * scale)
    body = Arc(radius=0.40 * scale, start_angle=20 * DEGREES, angle=140 * DEGREES,
               color=GREY, stroke_width=3, arc_center=c + DOWN * 0.18 * scale)
    return VGroup(head, body).set_opacity(0.72)


def population_bowl(blue_ids=BLUE_IDS, moving=True, people=True):
    """The carried population picture, always built at the same coordinates."""
    rim = Ellipse(width=5.15, height=3.95, stroke_color=GREY, stroke_width=5,
                  fill_color=GREY, fill_opacity=0.16).move_to(BOWL_C)
    rim.layout_ok = True
    cards = VGroup()
    for i, (x, y) in enumerate(CARD_POS):
        card = allele_card(BLUE if i in set(blue_ids) else GREY).move_to([x, y, 0])
        if moving:
            bob(card, amp=0.075, speed=1.35 + 0.07 * (i % 5), seed=i)
        cards.add(card)
    people_g = VGroup()
    if people:
        for p in [(-5.75, 2.65), (-4.35, 2.85), (-2.90, 2.85), (-1.55, 2.50)]:
            people_g.add(person_outline(p, 0.86))
    return VGroup(rim, cards, people_g)


def slot(center):
    return RoundedRectangle(corner_radius=0.11, width=1.18, height=0.82,
                            stroke_color=GREY, stroke_width=4, fill_color=BG, fill_opacity=0.92).move_to(center)


def genotype_display(left=BLUE, right=GREY, phenotype="neutral", heading=False):
    """The carried individual picture; slots, cards, and window never drift between scenes."""
    s1, s2 = slot(PAIR_C + LEFT * 0.72), slot(PAIR_C + RIGHT * 0.72)
    c1 = allele_card(left, 0.88, 0.52).move_to(s1)
    c2 = allele_card(right, 0.88, 0.52).move_to(s2)
    frame = RoundedRectangle(corner_radius=0.24, width=4.25, height=4.75,
                             stroke_color=GREY, stroke_width=3, fill_color=GREY,
                             fill_opacity=0.10).move_to([3.55, 0.15, 0])
    frame.layout_ok = True
    win_col = BLUE if phenotype == "blue" else GREY
    win_fill = 0.34 if phenotype in {"blue", "grey"} else 0.05
    window = RoundedRectangle(corner_radius=0.13, width=2.65, height=1.02,
                              stroke_color=win_col, stroke_width=4, fill_color=win_col,
                              fill_opacity=win_fill).move_to([3.55, -0.75, 0])
    word = "shows" if phenotype in {"blue", "grey"} else "waiting"
    wt = T(word, 32, win_col if phenotype != "neutral" else GREY, weight=BOLD).move_to(window)
    wt.layout_ok = True
    g = VGroup(frame, s1, s2, c1, c2, window, wt)
    g.slots, g.cards, g.window, g.word = VGroup(s1, s2), VGroup(c1, c2), window, wt
    if heading:
        h = T("one individual", 30, GREY).move_to([3.55, 2.82, 0])
        g.add(h)
    return g


def comparison_world(left=BLUE, right=GREY, phenotype="blue", blue_ids=BLUE_IDS, moving=True):
    return VGroup(population_bowl(blue_ids, moving=moving), genotype_display(left, right, phenotype, heading=True))


def predict_backdrop(moving=True):
    bowl = population_bowl(BLUE_IDS, moving=moving)
    pair = genotype_display(GREY, GREY, "neutral", heading=True)
    incoming = allele_card(BLUE, 0.88, 0.52).move_to([1.72, 1.05, 0])
    arrow = Arrow([2.15, 1.05, 0], [2.70, 1.05, 0], buff=0, color=TEAL,
                  stroke_width=5, tip_length=0.18)
    return VGroup(bowl, pair, incoming, arrow)


def trophy():
    cup = Arc(radius=0.55, start_angle=PI, angle=PI, color=GOLD, stroke_width=7)
    stem = Line([0, -0.52, 0], [0, -0.94, 0], color=GOLD, stroke_width=7)
    foot = Line([-0.35, -0.94, 0], [0.35, -0.94, 0], color=GOLD, stroke_width=7)
    handles = VGroup(Arc(radius=0.30, start_angle=-PI / 2, angle=PI, color=GOLD, stroke_width=5).shift(LEFT * 0.52),
                     Arc(radius=0.30, start_angle=PI / 2, angle=PI, color=GOLD, stroke_width=5).shift(RIGHT * 0.52))
    return VGroup(cup, stem, foot, handles)


def breathe_fill(mob, color, low=0.10, high=0.28, speed=1.7, seed=0.0):
    """Continuous slow activity for a large evidence container."""
    mob._fill_t = seed

    def update(m, dt):
        m._fill_t += dt
        opacity = low + (high - low) * (0.5 + 0.5 * np.sin(speed * m._fill_t))
        m.set_fill(color, opacity=opacity)
    return mob.add_updater(update)


class S00Hook(SpokenScene):
    def construct(self):
        bowl = population_bowl()
        tag = scope_tag("schematic")
        self.play(FadeIn(bowl, scale=0.96), FadeIn(tag), run_time=0.9)
        self.at("If an allele is dominant")
        blue = VGroup(*[bowl[1][i] for i in sorted(BLUE_IDS)])
        self.play(Indicate(blue, color=BLUE, scale_factor=1.18), run_time=0.7)
        q = T("?", 104, GOLD, weight=BOLD).move_to([-0.25, 1.45, 0])
        self.play(GrowFromCenter(q), run_time=0.65)
        self.at("Watch a few blue cards")
        self.play(blue.animate.shift(RIGHT * 0.28), run_time=0.55, rate_func=there_and_back)
        pulse(q, base=4, amp=1.5, speed=2.5)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Inherited or acquired?"
    TITLE = "Dominant Is Not Popular"

    def construct(self):
        bowl = population_bowl(moving=True).set_opacity(0.22)
        self.add(bowl)
        brand = T("BIOCHEMISTRYPEDIA", 20, TEAL, weight=BOLD).set_opacity(0.9)
        brand.layout_ok = True
        lesson = T(self.LESSON.upper(), 22, GREY)
        title = T(self.TITLE, 52, TEXT, font=TITLE_FONT)
        fit(title, max_w=11.5)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        card = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.30)
        self.play(FadeIn(card, shift=UP * 0.12), run_time=0.55)
        self.finish()


class S02Words(SpokenScene):
    def construct(self):
        bowl = population_bowl(moving=False, people=False).scale(0.70).move_to([-4.45, 0.45, 0])
        bob(bowl, amp=0.045, speed=1.25)
        parent_l = person_outline([1.45, 2.25, 0], 1.35)
        parent_r = person_outline([5.55, 2.25, 0], 1.35)
        pair = genotype_display(GREY, GREY, "neutral")
        self.add(bowl)
        self.at("An allele is a version")
        one = bowl[1][2]
        lab = T("allele", 30, BLUE, weight=BOLD).move_to([-4.45, 2.58, 0])
        self.play(Indicate(one, color=BLUE), FadeIn(lab), run_time=0.65)
        self.at("receives one copy")
        self.play(FadeIn(parent_l), FadeIn(parent_r), run_time=0.45)
        routes = VGroup(Arrow(parent_l.get_bottom(), pair.slots[0].get_top(), buff=0.12, color=TEAL, tip_length=0.18),
                        Arrow(parent_r.get_bottom(), pair.slots[1].get_top(), buff=0.12, color=TEAL, tip_length=0.18))
        self.play(FadeIn(pair[0]), FadeIn(pair.slots), GrowArrow(routes[0]), GrowArrow(routes[1]), run_time=0.8)
        self.play(FadeIn(pair.cards), run_time=0.55)
        self.at("The pair is its genotype")
        gl = T("genotype", 30, BLUE, weight=BOLD).next_to(pair.slots, DOWN, buff=0.18)
        self.play(FadeIn(gl), run_time=0.45)
        self.at("The trait that appears")
        self.play(FadeIn(pair.window), FadeIn(pair.word), run_time=0.55)
        pl = T("phenotype", 30, TEXT, weight=BOLD).next_to(pair.window, DOWN, buff=0.16)
        self.play(FadeIn(pl), run_time=0.45)
        self.at("Dominant and recessive")
        self.play(Indicate(pair.slots, color=BLUE, scale_factor=1.06), run_time=0.7)
        self.finish()


class S03ShowingRule(SpokenScene):
    def construct(self):
        bowl = population_bowl(moving=False, people=False).scale(0.66).move_to([-4.55, 0.55, 0])
        bob(bowl, amp=0.045, speed=1.25)
        pair = genotype_display(BLUE, GREY, "neutral", heading=True)
        self.add(bowl, pair)
        self.at("A dominant allele shows")
        blue_window = genotype_display(BLUE, GREY, "blue", heading=True)
        self.play(Transform(pair, blue_window), run_time=0.7)
        self.at("A recessive allele shows")
        grey_pair = genotype_display(GREY, GREY, "grey", heading=True)
        self.play(Transform(pair, grey_pair), run_time=0.8)
        self.at("So a dominant allele")
        masked = genotype_display(BLUE, GREY, "blue", heading=True)
        mask_bar = Line([3.35, 1.05, 0], [4.45, 1.05, 0], color=BLUE, stroke_width=8)
        self.play(Transform(pair, masked), Create(mask_bar), run_time=0.75)
        self.at("Neither word means stronger")
        gauge = dial(ValueTracker(0.5), center=[-1.0, -1.75, 0], radius=0.72,
                     label="strength", color=GOLD, fmt="neutral", scale=1, size=28)
        gauge[3].layout_ok = True
        gauge[4].layout_ok = True
        cross = Cross(gauge, stroke_color=RED, stroke_width=7)
        self.play(FadeIn(gauge), Create(cross), run_time=0.65)
        words = T("stronger   healthier   better", 28, GOLD).move_to([-1.0, -3.55, 0])
        self.play(FadeIn(words), run_time=0.45)
        self.finish()


class S04Predict(SpokenScene):
    def construct(self):
        world = predict_backdrop(moving=True)
        self.add(world, scope_tag("schematic"))
        self.at("When one blue card enters")
        incoming = world[2]
        self.play(incoming.animate.shift(RIGHT * 0.42), run_time=1.0)
        self.at("will its trait show")
        q = question_card("Will the trait show?", y=-3.15, size=32)
        self.play(FadeIn(q), run_time=0.5)
        self.at("Decide before the window changes")
        self.play(Indicate(incoming, color=BLUE, scale_factor=1.12), run_time=0.65)
        self.finish()


class S05Pause(PredictPause):
    QUESTION = "Will the trait show?"
    SECONDS = 4.5
    CARD = {"y": -3.15, "size": 32}
    RING_AT = (6.0, -2.45, 0)

    def backdrop(self):
        return VGroup(predict_backdrop(moving=True), scope_tag("schematic"))


class S06Reveal(SpokenScene):
    def construct(self):
        bowl = population_bowl(BLUE_IDS, moving=True)
        pair = genotype_display(GREY, GREY, "neutral", heading=True)
        incoming = allele_card(BLUE, 0.88, 0.52).move_to([2.14, 1.05, 0])
        self.add(bowl, pair, incoming, scope_tag("schematic"))
        self.at("The blue card enters")
        self.play(incoming.animate.move_to(pair.cards[0]), FadeOut(pair.cards[0]), run_time=0.75)
        self.at("and the trait shows")
        shown = genotype_display(BLUE, GREY, "blue", heading=True)
        self.play(Transform(pair, shown), FadeOut(incoming), run_time=0.7)
        self.at("That is dominance")
        individual = caption("shows in this individual", color=BLUE, y=-2.42)
        self.play(FadeIn(individual), run_time=0.45)
        self.at("Yet the population bowl")
        few = T("few blue cards", 28, GREY).move_to([-3.65, -3.05, 0])
        self.play(Indicate(VGroup(*[bowl[1][i] for i in sorted(BLUE_IDS)]), color=BLUE), FadeIn(few), run_time=0.75)
        self.at("The rule for showing changed")
        self.play(Indicate(pair.window, color=BLUE, scale_factor=1.08), run_time=0.65)
        self.at("did not make the allele common")
        common = T("common in this group: low", 28, GREY).move_to([-3.65, -3.05, 0])
        self.play(FadeOut(few), FadeIn(common), run_time=0.55)
        self.finish()


class S07IndependentControls(SpokenScene):
    def construct(self):
        bowl = population_bowl(BLUE_IDS, moving=True)
        pair = genotype_display(BLUE, GREY, "blue", heading=True)
        group_level, show_level = ValueTracker(0.16), ValueTracker(1.0)
        group_dial = dial(group_level, [-3.65, -1.95, 0], radius=0.72, label="group frequency",
                          color=BLUE, fmt="{:.0f}%", scale=100, size=27)
        show_dial = dial(show_level, [3.05, -1.95, 0], radius=0.72, label="shows in individual",
                         color=BLUE, fmt="{:.0f}%", scale=100, size=27)
        self.add(bowl, pair, group_dial, show_dial, scope_tag("schematic"))
        extras = VGroup(*[allele_card(BLUE).move_to([x, 3.35, 0]) for x in (-5.4, -4.65, -3.9, -3.15, -2.4)])
        self.at("move more blue cards into")
        targets = [[-5.1, 0.2, 0], [-4.35, 0.25, 0], [-3.55, 0.15, 0], [-2.8, 0.2, 0], [-2.2, -0.1, 0]]
        self.play(*[c.animate.move_to(t) for c, t in zip(extras, targets)], group_level.animate.set_value(0.72), run_time=1.1)
        self.at("The group display rises")
        self.play(Indicate(group_dial, color=BLUE), run_time=0.55)
        self.at("Move them out")
        self.play(*[c.animate.shift(UP * 4.5) for c in extras], group_level.animate.set_value(0.16), run_time=1.0)
        self.remove(*extras)
        self.at("individual display still follows")
        grey_pair = genotype_display(GREY, GREY, "grey", heading=True)
        self.play(Transform(pair, grey_pair), show_level.animate.set_value(0.0), run_time=0.75)
        blue_pair = genotype_display(BLUE, GREY, "blue", heading=True)
        self.play(Transform(pair, blue_pair), show_level.animate.set_value(1.0), run_time=0.75)
        self.at("Frequency belongs to the group")
        self.play(Indicate(VGroup(bowl, group_dial), color=BLUE, scale_factor=1.02), run_time=0.6)
        self.at("Dominance belongs")
        self.play(Indicate(VGroup(pair, show_dial), color=BLUE, scale_factor=1.02), run_time=0.6)
        self.finish()


class S08FourCases(SpokenScene):
    def construct(self):
        p = Plot(box=(-5.25, 5.15, -2.35, 2.65), xr=(0, 1), yr=(0, 1),
                 xlabel="showing rule: recessive  →  dominant", ylabel="group frequency",
                 color=GREY, size=24, label_size=28)
        mid_v = DashedLine(p.pt(0.5, 0), p.pt(0.5, 1), color=GREY, stroke_width=2)
        mid_h = DashedLine(p.pt(0, 0.5), p.pt(1, 0.5), color=GREY, stroke_width=2)
        rare = T("rare", 28, GREY).next_to(p.pt(0, 0.12), RIGHT, buff=0.18).shift(LEFT * 0.08)
        common = T("common", 28, GREY).next_to(p.pt(0, 0.88), RIGHT, buff=0.18)
        marker = VGroup(allele_card(BLUE, 1.0, 0.62), allele_card(GREY, 1.0, 0.62)).arrange(RIGHT, buff=0.13)
        marker.move_to(p.pt(0.82, 0.18))
        bowl_dot = Dot(p.pt(0.82, 0.18), radius=0.30, color=BLUE)
        high = RoundedRectangle(corner_radius=0.18, width=4.8, height=2.15,
                                stroke_width=0, fill_color=BLUE, fill_opacity=0.16).move_to(p.pt(0.75, 0.75))
        high.layout_ok = True
        self.add(high)
        self.play(Create(p), Create(mid_v), Create(mid_h), FadeIn(rare), FadeIn(common), run_time=0.9)
        self.add(scope_tag("schematic"))
        self.at("A dominant trait may be common")
        self.play(FadeIn(marker), FadeIn(bowl_dot), marker.animate.move_to(p.pt(0.82, 0.82)),
                  bowl_dot.animate.move_to(p.pt(0.82, 0.82)), run_time=0.85)
        low_right = high.copy().move_to(p.pt(0.75, 0.25))
        self.play(Transform(high, low_right), marker.animate.move_to(p.pt(0.82, 0.18)),
                  bowl_dot.animate.move_to(p.pt(0.82, 0.18)), run_time=0.65)
        self.at("A recessive trait may also")
        high_left = high.copy().move_to(p.pt(0.25, 0.75))
        self.play(Transform(high, high_left), marker.animate.move_to(p.pt(0.18, 0.18)),
                  bowl_dot.animate.move_to(p.pt(0.18, 0.82)), run_time=0.8)
        low_left = high.copy().move_to(p.pt(0.25, 0.25))
        self.play(Transform(high, low_left), bowl_dot.animate.move_to(p.pt(0.18, 0.18)), run_time=0.6)
        self.at("These are separate questions")
        divider = Line([0, -2.35, 0], [0, 2.65, 0], color=TEAL, stroke_width=5)
        whole_map = RoundedRectangle(corner_radius=0.18, width=10.2, height=4.55,
                                     stroke_width=0, fill_color=BLUE, fill_opacity=0.13).move_to([-0.05, 0.15, 0])
        whole_map.layout_ok = True
        self.play(Create(divider), Transform(high, whole_map), run_time=0.65)
        self.at("what an allele does")
        x_band = RoundedRectangle(corner_radius=0.18, width=10.2, height=1.25,
                                  stroke_width=0, fill_color=BLUE, fill_opacity=0.18).move_to([-0.05, -1.65, 0])
        x_band.layout_ok = True
        self.play(Transform(high, x_band), marker.animate.shift(RIGHT * 1.5),
                  run_time=0.75, rate_func=there_and_back)
        self.at("how many copies exist")
        y_band = RoundedRectangle(corner_radius=0.18, width=1.35, height=4.55,
                                  stroke_width=0, fill_color=BLUE, fill_opacity=0.18).move_to([-4.55, 0.15, 0])
        y_band.layout_ok = True
        self.play(Transform(high, y_band), bowl_dot.animate.shift(UP * 2.2),
                  run_time=0.80, rate_func=there_and_back)
        self.finish()


class S09NarrowMeaning(SpokenScene):
    def construct(self):
        bowl = population_bowl(BLUE_IDS, moving=False).scale(0.78).move_to([-3.95, 0.25, 0])
        bob(bowl, amp=0.045, speed=1.25)
        pair = genotype_display(BLUE, GREY, "blue", heading=True).scale(0.87).move_to([3.85, 0.25, 0])
        self.add(bowl, pair, scope_tag("schematic"))
        dom = T("dominant", 36, BLUE, weight=BOLD).move_to([1.65, 3.2, 0])
        cup = trophy().scale(0.65).move_to([-2.0, 2.65, 0])
        self.at("everyday word dominant")
        self.play(FadeIn(dom), cup.animate.shift(RIGHT * 1.1), run_time=0.65)
        self.at("sound like winning")
        barrier = Line([-0.65, 2.25, 0], [-0.65, 3.35, 0], color=RED, stroke_width=8)
        self.play(Create(barrier), cup.animate.shift(RIGHT * 0.20), run_time=0.45)
        win = T("winning", 28, GOLD).next_to(cup, DOWN, buff=0.12)
        self.play(FadeIn(win), run_time=0.25)
        self.play(FadeOut(VGroup(cup, win)), run_time=0.40)
        self.at("Genetics uses it more narrowly")
        self.play(dom.animate.move_to([3.85, 3.2, 0]), FadeOut(barrier), run_time=0.6)
        self.at("phenotype appears")
        self.play(Indicate(pair.window, color=BLUE), run_time=0.65)
        self.at("does not say one allele will spread")
        spread = Arrow([-0.3, 1.25, 0], [-1.55, 1.25, 0], color=BLUE, stroke_width=5, tip_length=0.2)
        stop = Line([-1.3, 0.75, 0], [-1.3, 1.75, 0], color=RED, stroke_width=7)
        sl = T("spread", 28, BLUE).next_to(spread, UP, buff=0.10).shift(UP * 0.50)
        self.play(GrowArrow(spread), FadeIn(sl), Create(stop), run_time=0.65)
        self.at("replace another")
        repl = T("replace", 28, BLUE).move_to([-0.15, 0.35, 0])
        self.play(FadeIn(repl), Indicate(stop, color=RED), run_time=0.5)
        self.at("or become common")
        self.play(Indicate(VGroup(*[bowl[1][i] for i in sorted(BLUE_IDS)]), color=BLUE), run_time=0.6)
        self.at("Population frequency is")
        measured = T("measure the group", 30, GREY, weight=BOLD).move_to([-3.95, -2.65, 0])
        self.play(FadeOut(VGroup(spread, sl, repl, stop)), FadeIn(measured), run_time=0.6)
        self.finish()


def small_family(center):
    x, y, _ = center
    parents = VGroup(person_outline([x - 0.9, y + 0.75, 0], 0.8), person_outline([x + 0.9, y + 0.75, 0], 0.8))
    child = person_outline([x, y - 0.75, 0], 0.8)
    routes = VGroup(Arrow([x - 0.65, y + 0.35, 0], [x - 0.12, y - 0.40, 0], color=TEAL, tip_length=0.16),
                    Arrow([x + 0.65, y + 0.35, 0], [x + 0.12, y - 0.40, 0], color=TEAL, tip_length=0.16))
    return VGroup(parents, child, routes)


class S10EvidenceBridge(SpokenScene):
    def construct(self):
        panels = TwoPanel("group frequency", "showing rule", colors=(BLUE, TEAL), top=3.0, bottom=-2.35)
        self.add(panels)
        count_box = RoundedRectangle(corner_radius=0.2, width=3.8, height=2.2,
                                     stroke_color=BLUE, stroke_width=4, fill_color=BLUE,
                                     fill_opacity=0.10).move_to([-3.3, -0.15, 0])
        family = small_family([3.3, 0.05, 0])
        self.at("count traits or alleles")
        self.play(FadeIn(count_box), run_time=0.45)
        breathe_fill(count_box, BLUE, low=0.09, high=0.25, speed=1.55)
        people = VGroup(*[person_outline([-5.4 + i * 0.72, 1.35, 0], 0.62) for i in range(6)])
        self.play(FadeIn(people), run_time=0.45)
        targets = [[-4.45 + (i % 3) * 1.15, 0.28 - (i // 3) * 0.8, 0] for i in range(6)]
        self.play(*[p.animate.move_to(t) for p, t in zip(people, targets)], run_time=1.0)
        self.at("To test dominance")
        self.play(FadeIn(family[0]), FadeIn(family[1]), run_time=0.5)
        self.at("follow which phenotypes appear")
        self.play(GrowArrow(family[2][0]), GrowArrow(family[2][1]), run_time=0.75)
        child_window = RoundedRectangle(corner_radius=0.10, width=1.55, height=0.62,
                                        stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.28).move_to([3.3, -1.45, 0])
        self.play(FadeIn(child_window), run_time=0.45)
        breathe_fill(child_window, BLUE, low=0.16, high=0.40, speed=1.8, seed=1.2)
        pulse(family[2], base=4.0, amp=1.8, speed=2.0)
        self.at("as Mendel did with peas")
        peas = VGroup(*[Circle(radius=0.12, color=GREEN, fill_color=GREEN, fill_opacity=0.4).shift(RIGHT * 0.30 * i) for i in range(3)]).move_to([5.15, -1.45, 0])
        self.play(FadeIn(peas), run_time=0.45)
        self.at("One kind of evidence cannot")
        divider = Line([0, -2.3, 0], [0, 2.3, 0], color=TEAL, stroke_width=6)
        self.play(Create(divider), run_time=0.55)
        self.at("Later courses add")
        later = T("more patterns later  →", 28, GREY).move_to([3.3, -2.85, 0])
        self.play(FadeIn(later), run_time=0.5)
        self.finish()


class S11Close(SpokenScene):
    def construct(self):
        bowl = population_bowl(BLUE_IDS, moving=False).scale(0.74).move_to([-3.9, 0.2, 0])
        bob(bowl, amp=0.045, speed=1.25)
        pair = genotype_display(BLUE, GREY, "blue", heading=False).scale(0.82).move_to([3.9, 0.2, 0])
        divider = Line([0, -2.75, 0], [0, 2.75, 0], color=TEAL, stroke_width=6)
        dom = T("dominant", 38, BLUE, weight=BOLD).move_to([3.9, 3.15, 0])
        common = T("common", 38, BLUE, weight=BOLD).move_to([-3.9, 3.15, 0])
        show_level, group_level = ValueTracker(0.92), ValueTracker(0.16)
        show_dial = dial(show_level, [3.9, -2.05, 0], radius=0.65, color=BLUE, fmt="shows", scale=1, size=26)
        group_dial = dial(group_level, [-3.9, -2.05, 0], radius=0.65, color=BLUE, fmt="few", scale=1, size=26)
        self.add(bowl, pair, divider, dom, common, show_dial, group_dial, scope_tag("schematic"))
        self.at("hear dominant")
        self.play(pair.animate.scale(1.12), bowl.animate.set_opacity(0.25), run_time=0.65)
        self.at("look inside one genotype pair")
        self.play(Indicate(pair.cards, color=BLUE, scale_factor=1.08), show_level.animate.set_value(0.72), run_time=0.7)
        self.at("Ask whether a copy shows")
        self.play(show_level.animate.set_value(1.0), Indicate(pair.window, color=BLUE), run_time=0.7)
        self.at("hear common")
        self.play(pair.animate.scale(1 / 1.12).set_opacity(0.25), bowl.animate.set_opacity(1.0).scale(1.08), run_time=0.7)
        self.at("look across the whole group")
        self.play(Indicate(bowl[1], color=BLUE, scale_factor=1.04), group_level.animate.set_value(0.28), run_time=0.7)
        self.at("Ask how often")
        self.play(group_level.animate.set_value(0.16), run_time=0.65)
        self.at("Never use one answer")
        self.play(FadeOut(VGroup(bowl, pair, show_dial, group_dial)), dom.animate.move_to([3.2, 0, 0]),
                  common.animate.move_to([-3.2, 0, 0]), run_time=0.75)
        self.finish()


class S12End(EndCard):
    LINE = "Dominant tells how an allele shows, not how common it is."
