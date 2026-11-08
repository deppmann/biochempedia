"""Living together: symbiosis  (Biochemistrypedia explainer, grade 7 Life Science)

COLOR MAP (one color per concept, whole video)
  BLUE   = fungus
  GREEN  = alga
  YELLOW = sugar
  TEAL   = "benefits"
  GREY   = bark / tree, "unaffected", structure, notes
  RED    = "harmed", blood lost
  PURPLE = tick (the parasite)
  TAN    = deer (the host)
  ORANGE = predator
  TEXT   = generic partners, kinds of symbiosis
No numbers on screen. All shapes are labelled schematic blocks, not to scale.
"""
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58AE0"
TAN = "#C9A27A"
ORANGE = "#E8935A"
LICHEN = "#9DB59A"
FUNGUS, ALGA, SUGAR, GAIN, HARM = BLUE, GREEN, YELLOW, TEAL, RED


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


class S00Title(TitleCard):
    LESSON = "Living together: symbiosis"
    TITLE = "Living Together: Help, Harm, or Neither"


# ---------------------------------------------------------------------------------------------
class S01Trunk(SpokenScene):
    def construct(self):
        trunk = Rectangle(width=3.0, height=6.2, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                          fill_opacity=0.18).move_to([-4.3, -0.1, 0])
        tl = T("tree trunk", 26, GREY).next_to(trunk, DOWN, buff=-0.45)
        tl.move_to([-4.3, -2.6, 0])
        patches = VGroup(*[Ellipse(width=w, height=h, stroke_color=LICHEN, stroke_width=3, fill_color=LICHEN,
                                   fill_opacity=0.55).move_to([x, y, 0])
                           for (w, h, x, y) in ((1.1, 0.8, -4.7, 1.8), (0.9, 0.7, -3.8, 0.4), (1.2, 0.8, -4.6, -1.0))])
        self.at("Look at")
        self.play(FadeIn(trunk), FadeIn(tl), run_time=1.0)
        self.at("crusty patches")
        self.play(FadeIn(patches, lag_ratio=0.3, scale=0.6), run_time=1.2)
        lab = chip("lichens", LICHEN, size=32).move_to([-4.3, 3.2, 0])
        self.at("are lichens")
        self.play(FadeIn(lab, shift=DOWN * 0.1), run_time=0.6)
        big = Ellipse(width=4.2, height=3.0, stroke_color=LICHEN, stroke_width=4, fill_color=LICHEN,
                      fill_opacity=0.45).move_to([2.6, 0.4, 0])
        one = T("one living thing?", 36, TEXT).move_to([2.6, -1.8, 0])
        self.at("Each lichen looks")
        self.play(TransformFromCopy(patches[1], big), run_time=1.2)
        self.play(FadeIn(one, shift=UP * 0.1), run_time=0.5)
        split = DashedLine([2.6, 1.9, 0], [2.6, -1.1, 0], color=TEXT, stroke_width=4)
        q1 = T("?", 72, TEXT, weight=BOLD).move_to([1.6, 0.4, 0])
        q2 = T("?", 72, TEXT, weight=BOLD).move_to([3.6, 0.4, 0])
        two = T("very different living things, one body", 30, TEXT).move_to([2.6, -2.5, 0])
        self.at("But it is a partnership")
        self.play(FadeOut(one), Create(split), FadeIn(q1, scale=0.6), FadeIn(q2, scale=0.6), run_time=1.0)
        self.play(FadeIn(two, shift=UP * 0.1), run_time=0.6)
        q = T("Do living things that live close together\nhelp each other, or hurt each other?", 38, TEXT,
              font=TITLE_FONT, line_spacing=0.8)
        fit(q, max_w=11.6, max_h=1.8)
        q.move_to([0, 0, 0])
        self.at("Do living things")
        self.play(*[FadeOut(m) for m in (trunk, tl, patches, lab, big, split, q1, q2, two)], run_time=0.7)
        self.play(Write(q), run_time=2.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Symbiosis(SpokenScene):
    def construct(self):
        title = T("symbiosis", 56, TEXT, font=TITLE_FONT).move_to([0, 3.0, 0])
        a = Circle(radius=0.7, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.12)
        b = Square(side_length=1.3, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.12)
        a.move_to([-5.0, 0.7, 0])
        b.move_to([5.0, 0.7, 0])
        la = T("species 1", 26, GREY).move_to([-0.95, 1.8, 0])
        lb = T("species 2", 26, GREY).move_to([0.95, 1.8, 0])
        self.at("Symbiosis is")
        self.play(FadeIn(title, shift=DOWN * 0.1), FadeIn(a), FadeIn(b), run_time=0.9)
        self.at("close relationship")
        self.play(a.animate.move_to([-0.95, 0.7, 0]), b.animate.move_to([0.95, 0.7, 0]),
                  run_time=0.8)
        self.at("different species")
        self.play(FadeIn(la), FadeIn(lb), run_time=0.5)
        link = Line(a.get_right(), b.get_left(), color=TEXT, stroke_width=6)
        self.add(link)
        time = Arrow([-5.5, -1.0, 0], [5.5, -1.0, 0], color=GREY, stroke_width=4, buff=0)
        tt = T("often a long time", 30, GREY).move_to([0, -1.6, 0])
        self.at("stay in close")
        grp = VGroup(a, b, la, lb, link)
        self.play(GrowArrow(time), FadeIn(tt), run_time=0.5)
        self.play(grp.animate.shift(LEFT * 3.2), run_time=0.5)
        self.play(grp.animate.shift(RIGHT * 6.4), run_time=0.9)
        self.at("A bird that eats")
        self.play(*[FadeOut(m) for m in (grp, time, tt)], run_time=0.4)
        bird = chip("bird", ORANGE, size=34).move_to([-2.0, 0.6, 0])
        seed = chip("one seed", GREEN, size=28).move_to([0.3, 0.6, 0])
        plant = chip("plant", GREEN, size=34).move_to([3.6, 0.6, 0])
        self.play(FadeIn(bird), FadeIn(seed), FadeIn(plant), run_time=0.4)
        self.play(seed.animate.move_to([0.4, -0.5, 0]), bird.animate.move_to([-1.5, -0.4, 0]), run_time=0.5)
        self.at("flies off")
        self.play(bird.animate.move_to([-5.4, 3.0, 0]), FadeOut(seed), run_time=0.7)
        cross = VGroup(Line([-0.5, -0.5, 0], [0.5, 0.5, 0]), Line([-0.5, 0.5, 0], [0.5, -0.5, 0])).set_color(GREY)
        cross.set_stroke(width=8).move_to([1.6, 0.6, 0])
        no = T("not a symbiosis", 40, TEXT).move_to([0, -2.2, 0])
        self.at("not in a symbiosis")
        self.play(Create(cross), FadeIn(no, shift=UP * 0.1), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Lichen(SpokenScene):
    def construct(self):
        cx = -1.6
        bark = Rectangle(width=8.4, height=0.9, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                         fill_opacity=0.25).move_to([cx, -2.5, 0])
        bl = T("tree bark", 28, GREY).move_to(bark)
        fungus = Rectangle(width=8.4, height=1.2, stroke_color=FUNGUS, stroke_width=3, fill_color=FUNGUS,
                           fill_opacity=0.25).move_to([cx, 1.2, 0])
        fl = T("fungus", 30, FUNGUS, weight=BOLD).move_to([5.0, 1.2, 0])
        cells = VGroup(*[Circle(radius=0.34, stroke_color=ALGA, stroke_width=3, fill_color=ALGA, fill_opacity=0.35)
                         .move_to([cx - 3.6 + i * 1.03, -0.5, 0]) for i in range(8)])
        al = T("alga", 30, ALGA, weight=BOLD).move_to([5.0, -0.5, 0])
        note = T("not to scale", 22, GREY).move_to([cx, -3.35, 0])
        self.at("A lichen is")
        self.play(FadeIn(bark), FadeIn(bl), FadeIn(note), run_time=0.4)
        self.at("a fungus")
        self.play(FadeIn(fungus, shift=DOWN * 0.2), FadeIn(fl), run_time=0.4)
        self.at("and an alga")
        self.play(FadeIn(cells, lag_ratio=0.05), FadeIn(al), run_time=0.5)
        br = Brace(VGroup(fungus, cells), direction=RIGHT, color=TEXT).shift(RIGHT * 0.1)
        brl = T("one body", 30, TEXT).next_to(br, RIGHT, buff=0.2)
        self.at("as one body")
        self.play(FadeOut(fl), FadeOut(al), run_time=0.1)
        fl2 = T("fungus", 28, FUNGUS, weight=BOLD).move_to([cx - 3.0, 1.2, 0])
        al2 = T("alga", 28, ALGA, weight=BOLD).move_to([cx - 3.0, -1.35, 0])
        self.play(FadeIn(fl2), FadeIn(al2), GrowFromCenter(br), FadeIn(brl), run_time=0.5)
        tiny = T("tiny, green", 28, ALGA).move_to([cx + 3.0, -1.35, 0])
        self.at("An alga is")
        self.play(Indicate(cells, color=ALGA), FadeIn(tiny, shift=UP * 0.1), run_time=0.6)
        self.at("The fungus forms")
        self.play(Indicate(fungus, color=FUNGUS, scale_factor=1.04), run_time=0.9)
        sh = VGroup(*[arr([cx - 2.4 + i * 2.4, 0.55, 0], [cx - 2.4 + i * 2.4, 0.0, 0], FUNGUS, w=4, tip=0.16) for i in range(3)])
        shl = T("shelters, helps keep moist", 26, FUNGUS).move_to([cx + 0.0, 2.35, 0])
        self.at("It shelters")
        self.play(FadeIn(sh, lag_ratio=0.2), FadeIn(shl, shift=DOWN * 0.1), run_time=1.0)
        self.at("The alga makes")
        self.play(FadeOut(tiny), FadeOut(shl), FadeOut(sh), run_time=0.4)
        sug = VGroup(*[chip("sugar", SUGAR, size=22, pad=0.1).move_to(cells[i].get_center() + UP * 0.68) for i in (3, 5, 7)])
        self.play(FadeIn(sug, scale=0.6), run_time=0.6)
        self.play(*[s.animate.move_to([s.get_center()[0], 1.2, 0]) for s in sug], run_time=1.4)
        self.at("feeds both partners")
        keep = VGroup(*[chip("sugar", SUGAR, size=22, pad=0.1).move_to(cells[i].get_center() + DOWN * 0.8) for i in (2, 4, 6)])
        self.play(FadeIn(keep, scale=0.6), Indicate(fungus, color=SUGAR, scale_factor=1.04), Indicate(cells, color=SUGAR), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
def column(cx, name, ca, ta, ca_col, cb, tb, cb_col, ex):
    card = RoundedRectangle(corner_radius=0.2, width=3.9, height=5.6, stroke_color=GREY, stroke_width=2.5,
                            fill_color=GREY, fill_opacity=0.06).move_to([cx, -0.4, 0])
    head = T(name, 34, TEXT, font=TITLE_FONT).move_to([cx, 1.85, 0])
    pa = chip(ca, ca_col, size=28).move_to([cx, 0.7, 0])
    pb = chip(cb, cb_col, size=28).move_to([cx, -0.95, 0])
    colr = {"benefits": GAIN, "unaffected": GREY, "harmed": HARM}
    tga = T(ta, 30, colr[ta], weight=BOLD).move_to([cx, 0.0, 0])
    tgb = T(tb, 30, colr[tb], weight=BOLD).move_to([cx, -1.65, 0])
    exl = T(ex, 24, GREY).move_to([cx, -2.6, 0])
    fit(exl, max_w=3.6)
    return card, head, pa, tga, pb, tgb, exl


class S04Three(SpokenScene):
    def construct(self):
        top = T("what does each partner gain or lose?", 32, GREY).move_to([0, 3.1, 0])
        c1 = column(-4.3, "mutualism", "fungus", "benefits", FUNGUS, "alga", "benefits", ALGA, "fungus and alga in a lichen")
        c2 = column(0.0, "commensalism", "lichen", "benefits", LICHEN, "tree", "unaffected", GREY, "lichen on tree bark")
        c3 = column(4.3, "parasitism", "one partner", "benefits", TEXT, "the other", "harmed", TEXT, "")
        self.at("Scientists sort")
        self.play(FadeIn(top, shift=DOWN * 0.1), run_time=0.8)
        self.at("In mutualism")
        self.play(FadeIn(c1[0]), FadeIn(c1[1]), FadeIn(c1[2]), FadeIn(c1[4]), run_time=0.9)
        self.at("all the partners benefit")
        self.play(FadeIn(c1[3], scale=0.8), FadeIn(c1[5], scale=0.8), FadeIn(c1[6]), run_time=0.9)
        self.at("In commensalism")
        self.play(FadeIn(c2[0]), FadeIn(c2[1]), FadeIn(c2[2]), FadeIn(c2[4]), run_time=0.9)
        self.at("one partner benefits")
        self.play(FadeIn(c2[3], scale=0.8), run_time=0.6)
        self.at("are unaffected")
        self.play(FadeIn(c2[5], scale=0.8), run_time=0.6)
        self.at("A lichen on tree bark")
        self.play(FadeIn(c2[6]), Indicate(c2[2], color=LICHEN), run_time=0.9)
        self.at("In parasitism")
        self.play(FadeIn(c3[0]), FadeIn(c3[1]), FadeIn(c3[2]), FadeIn(c3[4]), run_time=0.9)
        self.at("one partner benefits and the others are harmed")
        self.play(FadeIn(c3[3], scale=0.8), run_time=0.6)
        self.at("harmed")
        self.play(FadeIn(c3[5], scale=0.8), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Tick(SpokenScene):
    def construct(self):
        deer = RoundedRectangle(corner_radius=0.3, width=5.4, height=2.6, stroke_color=TAN, stroke_width=4,
                                fill_color=TAN, fill_opacity=0.2).move_to([-3.0, -0.6, 0])
        dl = T("deer", 40, TAN, weight=BOLD).move_to(deer)
        tick = chip("tick", PURPLE, size=28).move_to([-3.0, 1.9, 0])
        self.at("A black")
        self.play(FadeIn(deer), FadeIn(dl), FadeIn(tick, shift=DOWN * 0.3), run_time=0.5)
        drops = VGroup(*[Circle(radius=0.12, stroke_color=HARM, stroke_width=2, fill_color=HARM, fill_opacity=0.8)
                         .move_to([-3.0 + dx, 0.95, 0]) for dx in (-0.4, 0.0, 0.4)])
        bl = T("blood", 28, HARM).move_to([-1.2, 1.1, 0])
        self.at("drink blood")
        self.play(FadeIn(drops, lag_ratio=0.2), FadeIn(bl), run_time=0.4)
        self.play(*[d.animate.shift(UP * 0.35) for d in drops], run_time=0.5)
        days = T("several days", 34, TEXT).move_to([-3.0, -2.8, 0])
        self.at("several days")
        self.play(FadeIn(days, shift=UP * 0.1), run_time=0.6)
        pt = T("parasite", 34, PURPLE, weight=BOLD).move_to([-0.9, 1.9, 0])
        self.at("The tick is")
        self.play(FadeIn(pt, shift=DOWN * 0.1), Indicate(tick, color=PURPLE), run_time=0.6)
        ht = T("host", 34, TAN, weight=BOLD).move_to([-5.0, 1.1, 0])
        hd = T("the living thing a parasite\nlives on or in", 26, GREY, line_spacing=0.8).move_to([3.6, 0.3, 0])
        self.at("The deer is its host")
        self.play(FadeIn(ht, shift=RIGHT * 0.1), Indicate(deer, color=TAN, scale_factor=1.03), run_time=0.8)
        self.at("the living thing")
        self.play(FadeIn(hd, shift=LEFT * 0.1), run_time=0.7)
        self.at("A parasite usually")
        self.play(*[FadeOut(m) for m in (deer, dl, tick, drops, bl, days, pt, ht, hd)], run_time=0.6)
        r1 = T("parasite", 32, PURPLE, weight=BOLD).move_to([-4.9, 1.3, 0])
        b1 = Rectangle(width=7.0, height=0.5, stroke_color=PURPLE, stroke_width=3, fill_color=PURPLE,
                       fill_opacity=0.5).move_to([-1.1 + 0.0, 1.3, 0])
        b1.align_to([-3.6, 0, 0], LEFT)
        t1 = T("feeds over days or longer,\nusually without killing its host", 26, PURPLE).move_to([0.3, 0.55, 0])
        r2 = T("predator", 32, ORANGE, weight=BOLD).move_to([-4.9, -1.2, 0])
        b2 = Rectangle(width=1.2, height=0.5, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE,
                       fill_opacity=0.5)
        b2.align_to([-3.6, 0, 0], LEFT).set_y(-1.2)
        t2 = T("kills and eats its prey quickly", 26, ORANGE).move_to([0.3, -1.95, 0])
        t2.align_to(b2, LEFT)
        ax = Arrow([-3.6, -2.7, 0], [3.7, -2.7, 0], color=GREY, stroke_width=3, buff=0)
        axl = T("time (a sketch, not to scale)", 24, GREY).move_to([0.0, -3.15, 0])
        self.play(FadeIn(r1), FadeIn(r2), GrowArrow(ax), FadeIn(axl), run_time=0.7)
        self.play(GrowFromEdge(b1, LEFT), run_time=1.4)
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.6)
        self.at("A predator kills")
        self.play(GrowFromEdge(b2, LEFT), FadeIn(t2, shift=UP * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
def row(y, name, ta, tb):
    colr = {"benefits": GAIN, "unaffected": GREY, "harmed": HARM}
    n = chip(name, TEXT, size=32).move_to([-4.0, y, 0])
    a = chip(ta, colr[ta], size=28).move_to([0.6, y, 0])
    b = chip(tb, colr[tb], size=28).move_to([3.7, y, 0])
    n.align_to([-5.9, 0, 0], LEFT)
    return n, a, b


class S06Answer(SpokenScene):
    def construct(self):
        q = T("Do close partners help each other?", 38, TEXT, font=TITLE_FONT).move_to([0, 3.0, 0])
        self.at("So")
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.8)
        r1, r2, r3 = row(1.5, "mutualism", "benefits", "benefits"), row(0.2, "commensalism", "benefits", "unaffected"), \
            row(-1.1, "parasitism", "benefits", "harmed")
        self.at("Sometimes both partners benefit")
        self.play(*[FadeIn(m, shift=RIGHT * 0.1) for m in r1], run_time=0.9)
        self.at("Sometimes one benefits")
        self.play(*[FadeIn(m, shift=RIGHT * 0.1) for m in r2], run_time=0.9)
        self.at("Sometimes one is harmed")
        self.play(*[FadeIn(m, shift=RIGHT * 0.1) for m in r3], run_time=0.9)
        allrows = VGroup(q, *r1, *r2, *r3)
        self.at("Partners do not choose")
        self.play(FadeOut(allrows), run_time=0.6)
        kind = chip("choose to be kind", GREY, size=44).move_to([0, 0.5, 0])
        self.play(FadeIn(kind, scale=0.9), run_time=0.5)
        cross = VGroup(Line([-3.0, -0.5, 0], [3.0, 1.5, 0]), Line([-3.0, 1.5, 0], [3.0, -0.5, 0])).set_color(HARM)
        cross.set_stroke(width=7)
        self.play(Create(cross), run_time=0.7)
        self.at("carries on because")
        self.play(FadeOut(kind), FadeOut(cross), run_time=0.5)
        c1 = chip("living this way", TEXT, size=28)
        c2 = chip("let the partners (or at least\nthe parasite) survive and reproduce", GAIN, size=28)
        c3 = chip("the symbiosis carries on", TEXT, size=28)
        ch = VGroup(c1, c2, c3).arrange(DOWN, buff=0.9).move_to([0, 0.2, 0])
        a1 = arr(c1.get_bottom(), c2.get_top(), GREY, w=5)
        a2 = arr(c2.get_bottom(), c3.get_top(), GREY, w=5)
        self.play(FadeIn(c1, scale=0.9), run_time=0.6)
        self.at("survive and reproduce")
        self.play(GrowArrow(a1), FadeIn(c2, scale=0.9), run_time=0.8)
        self.play(GrowArrow(a2), FadeIn(c3, scale=0.9), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Living close together can help both, help one, or harm one."
