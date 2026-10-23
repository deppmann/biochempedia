"""Wood is built from air and water  (grade 7 Life Science explainer, photosynthesis-feeds-the-world)

COLOR MAP (one color per concept, whole video)
  PURPLE = carbon dioxide
  TEAL   = water
  YELLOW = light (radiant energy, sunlight)
  GOLD   = sugar (glucose)
  BLUE   = oxygen
  GREEN  = plants, producers, chloroplast, photosynthesis
  ORANGE = wood (the tree's dry wood)
  BROWN  = soil (and its minerals)
  RED    = heat (temperature), "cannot" crosses
  GREY   = outlines, structure, notes
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
BROWN = "#A47B52"

GROUND_Y = -2.0
TREE_X = 0.5


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=14)


def ground(label=True):
    g = RoundedRectangle(corner_radius=0.1, width=12.4, height=0.7, stroke_color=BROWN, stroke_width=3,
                         fill_color=BROWN, fill_opacity=0.3).move_to([0, GROUND_Y, 0])
    if not label:
        return g
    lab = T("soil", 26, BROWN).move_to([-5.2, GROUND_Y, 0])
    return VGroup(g, lab)


def tree(x=TREE_X, wood_scale=1.0):
    trunk = Rectangle(width=0.5 * wood_scale, height=2.2, stroke_color=ORANGE, stroke_width=3,
                      fill_color=ORANGE, fill_opacity=0.55)
    trunk.move_to([x, GROUND_Y + 0.35 + 1.1, 0])
    canopy = Ellipse(width=3.8, height=2.2, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.25)
    canopy.move_to([x, GROUND_Y + 0.35 + 2.2 + 0.7, 0])
    lab = T("tulip poplar", 24, GREEN).move_to(canopy)
    return VGroup(trunk, canopy, lab)


def seed(x=-5.0):
    s = Ellipse(width=0.34, height=0.22, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.8)
    return s.move_to([x, GROUND_Y + 0.35 + 0.11, 0])


class S00Title(TitleCard):
    LESSON = "Photosynthesis feeds the world"
    TITLE = "Wood Is Built Mostly From Air and Water"


# ---------------------------------------------------------------------------------------------
class S01Seed(SpokenScene):
    def construct(self):
        gr = ground()
        self.play(FadeIn(gr), run_time=0.5)
        sd = seed()
        sd_lab = T("seed: under 0.1 g", 26, TEXT).move_to([-4.6, -0.7, 0])
        sd_lab2 = T("(on average)", 24, GREY).next_to(sd_lab, DOWN, buff=0.12)
        self.at("seed weighs")
        self.play(FadeIn(sd, scale=2), FadeIn(sd_lab), FadeIn(sd_lab2), run_time=0.6)
        tr = tree()
        tr_lab = VGroup(T("about 10,000 kg", 30, ORANGE, weight=BOLD), T("of dry wood", 28, ORANGE)).arrange(DOWN, buff=0.1)
        tr_lab.move_to([4.5, 1.1, 0])
        self.at("grew so big")
        self.play(GrowFromPoint(tr, [TREE_X, GROUND_Y + 0.35, 0]), run_time=1.6)
        self.at("dry wood")
        self.play(FadeIn(tr_lab), run_time=0.5)
        note = VGroup(T("a model's estimate,", 24, GREY), T("not a weighing", 24, GREY)).arrange(DOWN, buff=0.08)
        note.next_to(tr_lab, DOWN, buff=0.35)
        self.at("estimate from a model")
        self.play(FadeIn(note), run_time=0.5)
        q = T("Where did all that wood come from?", 38, TEXT, font=TITLE_FONT).move_to([0, 3.15, 0])
        c1 = chip("from the air?", PURPLE, 26).move_to([-4.2, 1.7, 0])
        c2 = chip("from the soil?", BROWN, 26).move_to([-4.2, -0.4, 0])
        a1 = arr(c1.get_right(), [TREE_X - 1.9, 1.5, 0], PURPLE)
        a2 = arr(c2.get_right(), [TREE_X - 0.4, GROUND_Y + 1.4, 0], BROWN)
        self.at("where did all")
        self.play(FadeOut(VGroup(sd, sd_lab, sd_lab2)), FadeIn(q), run_time=0.6)
        self.play(FadeIn(c1), FadeIn(c2), GrowArrow(a1), GrowArrow(a2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Producer(SpokenScene):
    def construct(self):
        deer = chip("deer", GREY, 32).move_to([-4.0, 0.9, 0])
        food = chip("food", GREY, 28).move_to([-4.0, -1.6, 0])
        eat = arr(food.get_top(), deer.get_bottom(), GREY)
        eat_l = T("eats", 26, GREY).next_to(eat, RIGHT, buff=0.2)
        self.at("A deer")
        self.play(FadeIn(deer, shift=DOWN * 0.2), run_time=0.5)
        self.at("It has to eat")
        self.play(FadeIn(food), GrowArrow(eat), FadeIn(eat_l), run_time=0.7)
        plant = chip("plant", GREEN, 32).move_to([3.4, 0.9, 0])
        food2 = chip("food", GREY, 28).move_to([3.4, -1.6, 0]).set_opacity(0.35)
        eat2 = arr(food2.get_top(), plant.get_bottom(), GREY).set_opacity(0.35)
        cross = VGroup(Line(UL, DR, color=RED, stroke_width=7), Line(UR, DL, color=RED, stroke_width=7)).scale(0.28).move_to(eat2)
        self.at("A plant does not eat")
        self.play(FadeIn(plant, shift=DOWN * 0.2), FadeIn(food2), FadeIn(eat2), run_time=0.5)
        self.play(Create(cross), run_time=0.4)
        bar = Rectangle(width=0.5, height=0.3, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.5)
        bar.move_to([5.4, -0.3, 0])
        up = T("grows", 26, GREEN).move_to([5.4, -0.8, 0])
        self.at("yet it grows")
        self.play(FadeIn(bar), FadeIn(up), run_time=0.3)
        self.play(bar.animate.stretch_to_fit_height(2.4, about_edge=DOWN).set_opacity(1), run_time=1.2)
        self.at("A producer is")
        word = T("producer", 54, GREEN, font=TITLE_FONT).move_to([0, 2.3, 0])
        defn = T("a living thing that makes its own food", 32, TEXT).next_to(word, DOWN, buff=0.3)
        self.play(FadeOut(VGroup(deer, food, eat, eat_l, plant, food2, eat2, cross, bar, up)), run_time=0.5)
        self.play(FadeIn(word, shift=UP * 0.1), FadeIn(defn), run_time=0.7)
        p1 = chip("green plants", GREEN, 28).move_to([-4.2, -0.5, 0])
        p2 = chip("algae", GREEN, 28).move_to([-0.5, -0.5, 0])
        p3 = chip("phytoplankton", GREEN, 28).move_to([3.8, -0.5, 0])
        self.at("Green plants")
        self.play(FadeIn(p1, shift=UP * 0.2), run_time=0.4)
        self.at("algae")
        self.play(FadeIn(p2, shift=UP * 0.2), run_time=0.4)
        self.at("and phytoplankton")
        self.play(FadeIn(p3, shift=UP * 0.2), run_time=0.4)
        tiny = T("tiny producers that drift in water", 26, GREY).next_to(p3, DOWN, buff=0.3).shift(LEFT * 0.6)
        self.at("tiny producers")
        self.play(FadeIn(tiny), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Photo(SpokenScene):
    def construct(self):
        mid = [0, 0.2, 0]
        ax = arr([-1.6, 0.2, 0], [1.6, 0.2, 0], GREEN, w=9, tip=0.35)
        pname = T("photosynthesis", 36, GREEN, weight=BOLD).move_to([0, 1.0, 0])
        self.at("make food by")
        self.play(GrowArrow(ax), FadeIn(pname), run_time=0.8)
        sun = Circle(radius=0.32, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9).move_to([-5.6, 1.7, 0])
        sun_l = T("sunlight", 26, YELLOW).next_to(sun, DOWN, buff=0.15)
        ray = arr([-5.1, 1.6, 0], [-2.0, 0.4, 0], YELLOW, w=6)
        self.at("energy of sunlight")
        self.play(FadeIn(sun), FadeIn(sun_l), GrowArrow(ray), run_time=0.8)
        co2 = chip("carbon dioxide", PURPLE, 28).move_to([-4.3, 0.0, 0])
        wat = chip("water", TEAL, 28).move_to([-4.3, -1.5, 0])
        self.at("carbon dioxide and water")
        self.play(FadeIn(co2, shift=RIGHT * 0.3), run_time=0.5)
        self.play(FadeIn(wat, shift=RIGHT * 0.3), run_time=0.5)
        sug = chip("sugar (glucose)", GOLD, 28).move_to([4.2, 0.9, 0])
        oxy = chip("oxygen", BLUE, 28).move_to([4.2, -0.8, 0])
        self.at("sugar and oxygen")
        self.play(FadeIn(sug, shift=RIGHT * 0.3), run_time=0.5)
        self.play(FadeIn(oxy, shift=RIGHT * 0.3), run_time=0.5)
        rad = chip("radiant energy", YELLOW, 28).move_to([-3.6, 3.0, 0])
        self.at("radiant energy")
        self.play(ReplacementTransform(sun_l.copy(), rad), run_time=0.6)
        trav_l = T("energy that travels as light", 26, YELLOW).move_to([1.6, 3.0, 0])
        dot = Dot([-5.1, 1.6, 0], radius=0.12, color=YELLOW)
        self.at("travels as light")
        self.play(FadeIn(trav_l), FadeIn(dot), run_time=0.4)
        self.play(dot.animate.move_to([-2.0, 0.4, 0]), run_time=0.9, rate_func=linear)
        self.play(FadeOut(dot), run_time=0.1)
        note = T("a small sugar molecule that stores energy", 26, GOLD).move_to([3.4, -2.2, 0])
        self.at("a small sugar molecule")
        self.play(Indicate(sug, color=GOLD, scale_factor=1.1), FadeIn(note), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Where(SpokenScene):
    def construct(self):
        cell = RoundedRectangle(corner_radius=0.5, width=8.0, height=5.6, stroke_color=GREY, stroke_width=4,
                                fill_color=GREY, fill_opacity=0.06)
        cell_l = T("leaf cell", 28, GREY).move_to(cell.get_corner(UR) + LEFT * 1.2 + DOWN * 0.4)
        chl = Ellipse(width=5.6, height=3.2, stroke_color=GREEN, stroke_width=5, fill_color=GREEN, fill_opacity=0.3)
        chl.move_to(cell.get_center() + DOWN * 0.2)
        chl_l = T("chloroplast", 36, GREEN, weight=BOLD).move_to(chl.get_center() + UP * 0.5)
        self.at("chloroplast")
        self.play(FadeIn(cell), FadeIn(cell_l), run_time=0.5)
        self.play(GrowFromCenter(chl), FadeIn(chl_l), run_time=0.8)
        pig = T("chlorophyll: green pigment", 28, GREEN).move_to(chl.get_center() + DOWN * 0.3)
        glow = arr(cell.get_left() + RIGHT * 0.3 + UP * 1.9, chl.get_left() + RIGHT * 0.3 + UP * 0.8, YELLOW, w=6)
        glow_l = T("radiant energy", 26, YELLOW).move_to(cell.get_center() + LEFT * 1.4 + UP * 2.3)
        self.at("It holds chlorophyll")
        self.play(FadeIn(pig), run_time=0.5)
        self.at("captures radiant energy")
        self.play(FadeIn(glow_l), GrowArrow(glow), run_time=0.7)
        self.play(FadeOut(glow), FadeOut(glow_l), run_time=0.3)
        # plant cross-section on the left
        cell_g = VGroup(cell, cell_l, chl, chl_l, pig)
        scell = RoundedRectangle(corner_radius=0.4, width=5.4, height=3.6, stroke_color=GREY, stroke_width=4,
                                 fill_color=GREY, fill_opacity=0.06).move_to([3.5, 0.6, 0])
        schl = Ellipse(width=3.6, height=2.0, stroke_color=GREEN, stroke_width=5, fill_color=GREEN, fill_opacity=0.3).move_to([3.5, 0.45, 0])
        schl_l = T("chloroplast", 28, GREEN, weight=BOLD).move_to(schl)
        small = VGroup(scell, schl, schl_l)
        soil = Rectangle(width=5.2, height=1.5, stroke_color=BROWN, stroke_width=3, fill_color=BROWN, fill_opacity=0.3).move_to([-3.6, -2.6, 0])
        soil_l = T("soil", 26, BROWN).move_to(soil.get_corner(DL) + RIGHT * 0.5 + UP * 0.3)
        stem = Rectangle(width=0.45, height=2.8, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.35).move_to([-3.6, -0.5, 0])
        leaf = RoundedRectangle(corner_radius=0.3, width=3.2, height=1.1, stroke_color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.3).move_to([-3.6, 1.3, 0])
        leaf_l = T("leaf", 26, GREEN).move_to(leaf)
        root = VGroup(*[Line([-3.6, -1.9, 0], [-3.6 + dx, -3.1, 0], color=BROWN, stroke_width=4) for dx in (-1.2, -0.5, 0.5, 1.2)])
        plant = VGroup(soil, soil_l, root, stem, leaf, leaf_l)
        self.at("Roots take in water")
        sm_lab = T("one leaf cell, zoomed in", 26, GREY).move_to([3.5, -1.6, 0])
        self.play(FadeOut(cell_g), FadeIn(small), run_time=0.7)
        self.play(FadeIn(plant), FadeIn(sm_lab), run_time=0.8)
        wat = arr([-3.6, -2.5, 0], [-3.6, -0.4, 0], TEAL, w=8, tip=0.3)
        wat_l = T("water", 26, TEAL).move_to([-2.3, -1.2, 0])
        self.play(GrowArrow(wat), FadeIn(wat_l), run_time=0.8)
        co2 = arr([-6.2, 2.9, 0], [-4.5, 1.7, 0], PURPLE, w=8, tip=0.3)
        co2_l = T("carbon dioxide", 26, PURPLE).move_to([-4.6, 3.1, 0])
        self.at("Leaves take in carbon dioxide")
        self.play(GrowArrow(co2), FadeIn(co2_l), run_time=0.8)
        # air bar
        self.at("Carbon dioxide is only")
        clear = VGroup(small, sm_lab, plant, wat, wat_l, co2, co2_l)
        self.play(FadeOut(clear), run_time=0.5)
        bar = Rectangle(width=10.0, height=0.9, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.2).move_to([0, 0.6, 0])
        air_l = T("air", 34, TEXT).move_to([0, 1.6, 0])
        tick = Line(bar.get_corner(DL) + RIGHT * 0.1, bar.get_corner(UL) + RIGHT * 0.1, color=PURPLE, stroke_width=6)
        tick_l = T("carbon dioxide: about 0.04 percent of air", 30, PURPLE).move_to([0, -1.1, 0])
        tl = arr([-3.4, -0.9, 0], tick.get_bottom() + DOWN * 0.1, PURPLE, w=4, tip=0.2)
        ns = T("(not to scale)", 24, GREY).move_to([0, -1.9, 0])
        self.play(FadeIn(bar), FadeIn(air_l), run_time=0.5)
        self.at("tiny part of air")
        self.play(Create(tick), FadeIn(tick_l), GrowArrow(tl), FadeIn(ns), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Sugar(SpokenScene):
    def construct(self):
        sug = chip("sugar (glucose)", GOLD, 30).move_to([-4.6, 0.6, 0])
        self.at("Once a plant has sugar")
        self.play(FadeIn(sug, scale=0.9), run_time=0.6)
        use = chip("use it now", TEXT, 28).move_to([0.6, 2.2, 0])
        sto = chip("store it as starch", TEXT, 28).move_to([0.6, 0.6, 0])
        rea = chip("rearrange it", TEXT, 28).move_to([0.6, -1.0, 0])
        a1 = arr(sug.get_right() + UP * 0.2, use.get_left(), GOLD, w=5)
        a2 = arr(sug.get_right(), sto.get_left(), GOLD, w=5)
        a3 = arr(sug.get_right() + DOWN * 0.2, rea.get_left(), GOLD, w=5)
        self.at("It can use it now")
        self.play(GrowArrow(a1), FadeIn(use), run_time=0.6)
        self.at("store it as starch")
        self.play(GrowArrow(a2), FadeIn(sto), run_time=0.6)
        self.at("rearrange it")
        self.play(GrowArrow(a3), FadeIn(rea), run_time=0.6)
        wood = chip("wood of the trunk", ORANGE, 26).move_to([4.2, -0.3, 0])
        lv = chip("parts of new leaves", GREEN, 26).move_to([4.2, -1.7, 0])
        b1 = arr(rea.get_right(), wood.get_left(), GOLD, w=4)
        b2 = arr(rea.get_right(), lv.get_left(), GOLD, w=4)
        self.at("such as the wood")
        self.play(GrowArrow(b1), FadeIn(wood), run_time=0.5)
        self.play(GrowArrow(b2), FadeIn(lv), run_time=0.5)
        li = chip("light", YELLOW, 34)
        co = chip("carbon dioxide", PURPLE, 34)
        te = chip("temperature", RED, 34)
        cap = T("change how fast photosynthesis goes", 32, GREY).move_to([0, -3.0, 0])
        self.at("Light, carbon dioxide")
        row = VGroup(li, co, te)
        self.play(FadeOut(VGroup(a1, a2, a3, use, sto, rea, b1, b2, wood, lv, sug)), run_time=0.5)
        li.move_to([-4.6, 0.8, 0]); co.move_to([-0.3, 0.8, 0]); te.move_to([4.2, 0.8, 0])
        self.play(FadeIn(li), run_time=0.4)
        self.play(FadeIn(co), run_time=0.4)
        self.play(FadeIn(te), run_time=0.4)
        cap.move_to([0, -0.6, 0])
        self.at("change how fast")
        self.play(FadeIn(cap), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        gr = ground()
        tr = tree()
        q = T("Where did the tulip poplar's wood come from?", 36, TEXT, font=TITLE_FONT).move_to([0, 3.15, 0])
        self.add(gr, tr)
        self.play(FadeIn(q), run_time=0.5)
        co2 = chip("carbon dioxide", PURPLE, 26).move_to([-4.6, 1.9, 0])
        wat = chip("water", TEAL, 26).move_to([-3.0, GROUND_Y, 0])
        a1 = arr(co2.get_right(), [TREE_X - 1.9, 1.6, 0], PURPLE, w=6)
        a2 = arr(wat.get_right() + UP * 0.1, [TREE_X - 0.4, GROUND_Y + 1.0, 0], TEAL, w=6)
        self.at("built it mostly")
        self.play(FadeIn(co2), GrowArrow(a1), run_time=0.7)
        air = T("from the air", 24, PURPLE).next_to(co2, UP, buff=0.12)
        self.at("from the air")
        self.play(FadeIn(air), run_time=0.4)
        self.at("and from water")
        self.play(FadeIn(wat), GrowArrow(a2), run_time=0.7)
        rad = chip("radiant energy", YELLOW, 26).move_to([4.7, 2.0, 0])
        a3 = arr(rad.get_left(), [TREE_X + 1.9, 1.7, 0], YELLOW, w=6)
        self.at("Leaves used radiant energy")
        self.play(FadeIn(rad), GrowArrow(a3), run_time=0.7)
        sug = chip("sugar", GOLD, 26).move_to([TREE_X, GROUND_Y + 0.35 + 2.9, 0])
        self.at("join them into sugar")
        self.play(FadeOut(tr[2]), FadeIn(sug, scale=0.8), run_time=0.5)
        wood_lab = T("wood", 30, ORANGE, weight=BOLD).move_to([2.9, -0.5, 0])
        wood_a = arr(wood_lab.get_left() + LEFT * 0.0, [TREE_X + 0.55, -0.5, 0], ORANGE, w=5)
        self.at("rebuilt the sugar into wood")
        self.play(sug.animate.move_to([TREE_X, GROUND_Y + 1.5, 0]).scale(0.85), run_time=0.8)
        self.play(tr[0].animate.stretch_to_fit_width(0.9).set_fill(ORANGE, 0.9), FadeIn(wood_lab), GrowArrow(wood_a), FadeOut(sug), FadeIn(tr[2]), run_time=0.8)
        mins = T("water and a few minerals", 26, BROWN).move_to([2.6, -3.1, 0])
        self.at("soil gave water")
        self.play(FadeIn(mins), Indicate(gr[0], color=BROWN, scale_factor=1.03), run_time=0.8)
        self.play(mins.animate.move_to([0, -3.1, 0]), run_time=0.3)
        full = T("soil did not need to shrink by thousands of kg", 26, GREY).move_to([0, -3.1, 0])
        self.at("did not need to shrink")
        self.play(ReplacementTransform(mins, full), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "A tree builds wood mostly from carbon dioxide and water."
