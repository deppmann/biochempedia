"""Respiration and ATP: how the energy in food becomes energy a cell can use (high school Biology explainer)

COLOR MAP (one color per concept, whole video)
  YELLOW = glucose (the fuel)
  BLUE   = oxygen
  GREY   = carbon dioxide, outlines, small labels
  TEAL   = water
  GREEN  = ATP
  ORANGE = ADP
  PURPLE = phosphate group
  GOLD   = energy released / energy arrows
  PINK   = mitochondrion outline
  RED    = fermentation products (lactate, ethanol), crossed-out oxygen
  TEXT   = vocabulary words and the question
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
PINK = "#E58FB0"


def lab(text, pos, color=TEXT, size=26, weight=NORMAL):
    return T(text, size, color, weight=weight).move_to(pos)


def psq(pos, side=0.85):
    pos = [pos[0], pos[1], 0]
    sq = RoundedRectangle(corner_radius=0.1, width=side, height=side, stroke_color=PURPLE, stroke_width=3,
                          fill_color=PURPLE, fill_opacity=0.3)
    return VGroup(sq, T("P", 34, TEXT, weight=BOLD).move_to(sq)).move_to(pos)


def base_block(label, color, pos, w=2.4, h=1.2):
    pos = [pos[0], pos[1], 0]
    r = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color, stroke_width=4,
                         fill_color=color, fill_opacity=0.2)
    return VGroup(r, T(label, 28, TEXT).move_to(r)).move_to(pos)


# Compartments and arrows keep the original rounded schematic drawing style.
def mito(pos, w=3.5, h=2.0):
    r = RoundedRectangle(corner_radius=0.8, width=w, height=h,
                         stroke_color=PINK, stroke_width=5, fill_color=PINK, fill_opacity=0.1)
    return VGroup(r, T("mitochondrion", 26, PINK).move_to(r.get_top() + DOWN * 0.4)).move_to(pos)


def arrow(a, b, color=TEXT):
    return Arrow(a, b, color=color, stroke_width=5, buff=0.12)


def moving_chip(text, color, pos):
    g = chip(text, color, 26).move_to(pos)
    g[0].set_fill(BG, 1)  # Mask the route beneath the moving label.
    return g


class S00Title(TitleCard):
    LESSON = "Respiration and ATP"
    TITLE = "Food Energy Becomes ATP"


class S01Question(SpokenScene):
    def construct(self):
        cell = RoundedRectangle(corner_radius=0.6, width=9.6, height=4.3,
                                stroke_color=GREY, stroke_width=4).move_to([0.9, 0.6, 0])
        glucose = chip("glucose", YELLOW, 30).move_to([-5.2, 1.2, 0])
        atp = chip("ATP", GREEN, 38).move_to([4.0, 0.4, 0])
        self.at("Cells break down food")
        self.play(Create(cell), FadeIn(glucose), run_time=0.6)
        self.play(glucose.animate.move_to([-2.4, 0.4, 0]), run_time=0.7)
        self.at("to build")
        energy = arrow([-1.1, 0.4, 0], [3.0, 0.4, 0], GOLD)
        self.play(GrowArrow(energy), FadeIn(atp), run_time=0.7)
        self.at("carries energy")
        work = chip("cell work", TEXT, 30).move_to([4.0, -2.5, 0])
        delivery = arrow([4.0, -0.15, 0], [4.0, -1.9, 0], GOLD)
        self.play(GrowArrow(delivery), FadeIn(work), run_time=0.6)
        self.at("With oxygen")
        m = mito([0.3, 0.6, 0])
        oxygen = chip("oxygen", BLUE, 28).move_to([0.3, 3.1, 0])
        self.play(FadeOut(energy), FadeIn(oxygen), Create(m), run_time=0.5)
        self.play(oxygen.animate.move_to([0.3, 0.3, 0]), run_time=0.7)
        energy2 = arrow([2.1, 0.4, 0], [3.0, 0.4, 0], GOLD)
        self.at("most")
        self.play(GrowArrow(energy2), Indicate(atp, color=GREEN), run_time=0.7)
        title = lab("cellular respiration", [0.0, 3.1, 0], TEXT, 36, BOLD)
        self.at("This is cellular respiration")
        self.play(FadeIn(title), run_time=0.5)
        self.at("every working cell")
        idea = lab("Food energy reaches cell work through ATP", [0, -3.3, 0], GOLD, 28)
        self.play(FadeIn(idea), run_time=0.6)
        self.at("A muscle cell pulls")
        muscle = base_block("muscle pulls", TEXT, [-2.3, -2.3], w=3.6, h=0.8)
        self.play(ReplacementTransform(work, muscle), delivery.animate.put_start_and_end_on(
            [3.8, -0.3, 0], [-0.2, -2.3, 0]), run_time=0.5)
        self.play(muscle[0].animate.stretch(0.75, 0), run_time=0.5, rate_func=there_and_back)
        self.at("A nerve cell pumps")
        membrane = VGroup(Line([-3.6, -2.1, 0], [-0.8, -2.1, 0], color=GREY, stroke_width=8),
                          lab("membrane pumping", [-2.2, -2.8, 0], TEXT, 26))
        particle = chip("+", BLUE, 24, pad=0.1).move_to([-2.2, -2.5, 0])
        self.play(FadeOut(muscle), FadeIn(membrane), FadeIn(particle), run_time=0.4)
        self.play(particle.animate.move_to([-2.2, -1.7, 0]), run_time=0.7)
        self.at("Cells build proteins")
        protein = VGroup(*[RoundedRectangle(width=0.6, height=0.5, corner_radius=0.1,
                              stroke_color=TEXT, fill_color=TEXT, fill_opacity=0.2)
                              for _ in range(3)]).arrange(RIGHT, buff=0.15).move_to([-2.2, -2.1, 0])
        protein_l = lab("protein building", [-2.2, -2.8, 0], TEXT, 26)
        self.play(FadeOut(membrane), FadeOut(particle), FadeIn(protein_l),
                  LaggedStart(*[FadeIn(p, shift=LEFT * 0.2) for p in protein], lag_ratio=0.25), run_time=0.8)
        self.finish()


class S02Respire(SpokenScene):
    def construct(self):
        glucose = chip("glucose", YELLOW, 30).move_to([-4.9, 1.2, 0])
        oxygen = chip("oxygen", BLUE, 30).move_to([-2.2, 1.2, 0])
        products = VGroup(chip("carbon dioxide", GREY, 28), chip("water", TEAL, 28)).arrange(RIGHT, buff=0.35).move_to([3.0, 1.2, 0])
        plus = lab("+", [-3.5, 1.2, 0], TEXT, 32)
        reaction = arrow([-0.9, 1.2, 0], [0.3, 1.2, 0])
        self.at("Glucose is a sugar")
        self.play(FadeIn(glucose), run_time=0.6)
        self.at("With oxygen")
        self.play(FadeIn(plus), FadeIn(oxygen), run_time=0.5)
        self.at("it becomes")
        self.play(GrowArrow(reaction), FadeIn(products, shift=RIGHT * 0.2), run_time=0.7)
        atp = chip("ATP", GREEN, 36).move_to([-1.9, -1.3, 0])
        capture = arrow([0, 0.7, 0], [-1.9, -0.7, 0], GOLD)
        self.at("released energy")
        self.play(GrowArrow(capture), FadeIn(atp), run_time=0.7)
        heat = lab("heat", [2.4, -1.3, 0], GOLD, 32)
        loss = arrow([0.4, 0.7, 0], [2.4, -0.7, 0], GOLD)
        self.at("Some leaves as heat")
        self.play(GrowArrow(loss), FadeIn(heat), run_time=0.6)
        self.at("The first steps")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.35)
        cell = RoundedRectangle(corner_radius=0.6, width=11.6, height=4.8,
                                stroke_color=GREY, stroke_width=4).move_to([0, 0.3, 0])
        cyt = lab("cytoplasm", [-3.3, 1.85, 0], GREY, 30)
        first = chip("first steps", TEXT, 28).move_to([-3.3, 0.3, 0])
        self.play(Create(cell), FadeIn(cyt), FadeIn(first), run_time=0.6)
        self.at("Later steps")
        m = mito([2.6, 0.3, 0], 4.7, 3.0)
        later = lab("later steps", [2.6, -0.1, 0], TEXT, 28)
        flow = arrow([-1.8, 0.3, 0], [0.0, 0.3, 0], YELLOW)
        self.play(Create(m), FadeIn(later), GrowArrow(flow), run_time=0.7)
        self.at("organelles in plant")
        orgs = lab("plant  •  animal  •  fungal cells", [0, -2.8, 0], GREY, 30)
        self.play(FadeIn(orgs), run_time=0.5)
        self.at("Plants respire")
        plant = lab("plant cell", [0, 3.15, 0], TEXT, 34, BOLD)
        wall = RoundedRectangle(corner_radius=0.2, width=12.1, height=5.3,
                                stroke_color=GREY, stroke_width=3).move_to(cell)
        self.play(Create(wall), FadeIn(plant), Indicate(m, color=PINK, scale_factor=1.03), run_time=0.8)
        self.finish()


class S03Atp(SpokenScene):
    def construct(self):
        # Symbolic phosphate tiles, with no drawn chemical bonds or structure.
        ade = base_block("ATP", GREEN, [-3.9, 0.9], 2.6, 1.2)
        ps = [psq([-1.9 + i * 1.0, 0.9]) for i in range(3)]
        pl = lab("three phosphate groups", [-0.9, -0.15, 0], PURPLE, 26)
        self.at("A TP has")
        self.play(FadeIn(ade), run_time=0.3)
        self.at("three phosphate groups")
        self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.2) for p in ps], lag_ratio=0.2), FadeIn(pl), run_time=0.8)
        self.at("reacts with water")
        water = chip("water", TEAL, 28).move_to([3.5, 2.4, 0])
        self.play(FadeIn(water), run_time=0.3)
        self.play(water.animate.move_to([1.1, 2.0, 0]), run_time=0.6)
        self.at("comes off")
        phosphate = lab("phosphate", [3.9, -0.15, 0], PURPLE, 26)
        self.play(FadeOut(water), ps[2].animate.move_to([3.9, 0.9, 0]), FadeIn(phosphate), FadeOut(pl), run_time=0.7)
        self.at("What is left")
        adp = base_block("ADP", ORANGE, [-3.9, 0.9], 2.6, 1.2)
        two = lab("two phosphate groups", [-1.4, -0.15, 0], PURPLE, 26)
        self.play(Transform(ade, adp), FadeIn(two), run_time=0.6)
        self.at("The whole reaction")
        whole = VGroup(Line([-5.2, 2.0, 0], [4.5, 2.0, 0], color=GOLD, stroke_width=4),
                       lab("whole reaction releases energy", [0, 2.8, 0], GOLD, 32, BOLD))
        self.play(Create(whole), run_time=0.6)
        self.at("the cell uses for work")
        work = chip("cell work", TEXT, 30).move_to([0, -2.2, 0])
        en = arrow([0, -0.6, 0], [0, -1.6, 0], GOLD)
        self.play(GrowArrow(en), FadeIn(work), run_time=0.6)
        self.at("Breaking a bond")
        note = lab("Breaking a bond takes energy", [0, -3.2, 0], TEXT, 28)
        self.play(FadeIn(note), run_time=0.6)
        self.at("is not energy")
        self.play(FadeOut(whole), FadeOut(note), FadeOut(work), FadeOut(en), run_time=0.4)
        statement = lab("ATP is not energy", [0, -1.7, 0], TEXT, 34, BOLD)
        self.play(FadeIn(statement), run_time=0.5)
        self.at("It is a molecule")
        carries = lab("ATP is a molecule that carries energy", [0, -2.7, 0], GREEN, 30)
        self.play(FadeIn(carries), run_time=0.6)
        self.finish()


class S04Cycle(SpokenScene):
    def construct(self):
        atp = chip("ATP", GREEN, 44).move_to([-4.4, 0.4, 0])
        adp = chip("ADP + phosphate", ORANGE, 32).move_to([3.9, 0.4, 0])
        top = Arrow([-2.7, 1.0, 0], [1.6, 1.0, 0], color=TEXT, stroke_width=6, buff=0)
        bot = Arrow([1.6, -0.2, 0], [-2.7, -0.2, 0], color=GOLD, stroke_width=8, buff=0)
        bot_l = lab("respiration supplies energy", [-0.5, -1.05, 0], GOLD, 28, BOLD)
        top_l = VGroup(T("reacts with water", 28, TEAL),
                       T("supplies energy for cell work", 28, TEXT, weight=BOLD)
                       ).arrange(DOWN, buff=0.2).move_to([-0.5, 2.3, 0])
        requires = lab("rebuilding ATP requires energy", [0, 3.0, 0], GOLD, 32)
        self.at("Putting a phosphate")
        self.play(FadeIn(atp), FadeIn(adp), run_time=0.6)
        self.at("takes energy")
        self.play(GrowArrow(bot), FadeIn(requires), run_time=0.7)
        self.at("Cellular respiration supplies")
        self.play(FadeIn(bot_l), run_time=0.5)
        self.at("go round in a cycle")
        self.play(GrowArrow(top), run_time=0.6)
        self.at("Cell work turns")
        self.play(FadeOut(requires), FadeIn(top_l), run_time=0.5)
        moving = moving_chip("ATP", GREEN, [-2.8, 1.0, 0])
        self.play(FadeIn(moving), run_time=0.2)
        self.play(moving.animate.move_to([1.5, 1.0, 0]), run_time=0.6)
        self.play(Transform(moving, moving_chip("ADP", ORANGE, [1.5, 1.0, 0])), run_time=0.3)
        self.at("Respiration turns")
        self.play(moving.animate.move_to([1.5, -0.2, 0]), run_time=0.3)
        self.play(moving.animate.move_to([-2.7, -0.2, 0]), run_time=0.6)
        self.play(Transform(moving, moving_chip("ATP", GREEN, [-2.7, -0.2, 0])), run_time=0.3)
        self.play(FadeOut(moving), run_time=0.2)
        self.at("small supply")
        supply = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.8, height=0.5,
                              stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.3)
                              for _ in range(3)]).arrange(RIGHT, buff=0.12).move_to([0, -2.2, 0])
        supply_l = lab("small ATP supply • constantly rebuilt", [0, -3.05, 0], GREEN, 28)
        self.play(FadeIn(supply), FadeIn(supply_l), run_time=0.5)
        self.at("so it rebuilds")
        self.play(supply[0].animate.set_fill(GREEN, 0), run_time=0.25)
        self.play(supply[0].animate.set_fill(GREEN, 0.6), Indicate(bot, color=GOLD), run_time=0.4)
        self.at("all the time")
        self.play(supply[1].animate.set_fill(GREEN, 0), run_time=0.2)
        self.play(supply[1].animate.set_fill(GREEN, 0.6), run_time=0.3)
        self.finish()


class S05Ferment(SpokenScene):
    def construct(self):
        aerobic = VGroup(T("aerobic", 38, TEXT, weight=BOLD), T("uses oxygen", 28, BLUE)).arrange(DOWN, buff=0.2).move_to([-3.4, 2.4, 0])
        anaerobic = VGroup(T("anaerobic", 38, TEXT, weight=BOLD), T("without oxygen", 28, BLUE)).arrange(DOWN, buff=0.2).move_to([3.4, 2.4, 0])
        ferment = chip("fermentation", TEXT, 34).move_to([0, 0.0, 0])
        users = lab("muscle cells and yeast", [0, -1.0, 0], TEXT, 28)
        sol = lab("SOL term: anaerobic respiration", [0, -2.0, 0], GOLD, 28)
        self.at("Aerobic means")
        self.play(FadeIn(aerobic), run_time=0.5)
        self.at("Anaerobic means")
        self.play(FadeIn(anaerobic), run_time=0.5)
        # The first 'without oxygen' belongs to the definition, so cue the next beat by its users.
        self.at("muscle cells and yeast")
        self.play(FadeIn(ferment), FadeIn(users), run_time=0.7)
        self.at("calls this")
        self.play(FadeIn(sol), run_time=0.5)
        self.at("With oxygen")
        self.play(FadeOut(VGroup(ferment, users, sol)),
                  aerobic.animate.move_to([-3.4, 2.8, 0]), anaerobic.animate.move_to([3.4, 2.8, 0]), run_time=0.4)
        title = lab("ATP per glucose", [0, -3.0, 0], GREY, 30)
        animal = lab("animal cell", [-3.4, 1.8, 0], GREY, 26)
        b1 = Rectangle(width=1.6, height=3.1, stroke_color=GREEN, fill_color=GREEN,
                       fill_opacity=0.4).move_to([-3.4, -0.45, 0])
        n1 = lab("about 30 to 32", [-3.4, 1.35, 0], GREEN, 28, BOLD)
        self.play(FadeIn(title), FadeIn(animal), run_time=0.4)
        self.at("about 30 to 32")
        self.play(GrowFromEdge(b1, DOWN), FadeIn(n1), run_time=0.8)
        self.at("Fermentation gives")
        b2 = Rectangle(width=1.6, height=0.2, stroke_color=GREEN, fill_color=GREEN,
                       fill_opacity=0.4).move_to([3.4, -1.9, 0])
        n2 = lab("2", [3.4, -1.15, 0], GREEN, 38, BOLD)
        fl = lab("fermentation", [3.4, -2.4, 0], TEXT, 26)
        self.play(GrowFromEdge(b2, DOWN), FadeIn(n2), FadeIn(fl), run_time=0.7)
        self.at("In muscle")
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.35)
        source = chip("fermentation", TEXT, 32).move_to([-3.8, 0.4, 0])
        muscle = VGroup(lab("in muscle", [2.2, 2.5, 0], GREY, 28),
                        chip("lactate", RED, 30).move_to([2.2, 1.7, 0]))
        a1 = arrow([-1.8, 0.8, 0], [0.9, 1.7, 0])
        self.play(FadeIn(source), GrowArrow(a1), FadeIn(muscle), run_time=0.7)
        self.at("In yeast")
        yeast = VGroup(lab("in yeast", [2.2, 0.3, 0], GREY, 28),
                       chip("ethanol", RED, 28).move_to([1.0, -0.6, 0]),
                       chip("carbon dioxide", GREY, 26).move_to([4.1, -0.6, 0]))
        a2 = arrow([-1.8, 0.0, 0], [0.0, -0.5, 0])
        self.play(GrowArrow(a2), FadeIn(yeast), run_time=0.7)
        self.at("forms the bubbles")
        dough = Ellipse(width=3.1, height=0.9, stroke_color=TEXT, stroke_width=4,
                        fill_color=TEXT, fill_opacity=0.12).move_to([3.0, -2.4, 0])
        bubbles = VGroup(*[Circle(radius=r, stroke_color=TEXT, stroke_width=3).move_to([3.0 + dx, -2.4 + dy, 0])
                          for r, dx, dy in [(0.13, -0.8, 0), (0.2, 0, 0.1), (0.15, 0.7, -0.1)]])
        self.play(Create(dough), FadeIn(bubbles), run_time=0.5)
        self.at("make dough rise")
        dr = lab("dough rises", [-1.1, -2.4, 0], TEXT, 28)
        self.play(dough.animate.stretch(1.5, 1), bubbles.animate.shift(UP * 0.2).scale(1.2), FadeIn(dr), run_time=0.8)
        self.finish()


class S06Answer(SpokenScene):
    def construct(self):
        # Matter occupies the upper loop. Energy later follows a separate, open gold path.
        photo = base_block("photosynthesis", TEXT, [-3.9, 1.1], 3.5, 1.0)
        resp = base_block("respiration", TEXT, [3.9, 1.1], 3.5, 1.0)
        feed = VGroup(chip("carbon dioxide", GREY, 24), chip("water", TEAL, 24)).arrange(RIGHT, buff=0.25).move_to([0, -0.4, 0])
        glucose = chip("glucose", YELLOW, 26).move_to([-0.9, 2.7, 0])
        oxygen = chip("oxygen", BLUE, 26).move_to([1.5, 2.7, 0])
        for token in (glucose, oxygen, *feed):
            token[0].set_fill(BG, 1)
            token.set_z_index(2)
        light = lab("light energy", [-3.9, 3.35, 0], GOLD, 28)
        incoming = arrow([-3.9, 3.0, 0], [-3.9, 1.8, 0], GOLD)
        self.at("Photosynthesis uses")
        self.play(FadeIn(photo), FadeIn(light), GrowArrow(incoming), run_time=0.8)
        self.at("build glucose")
        self.play(FadeIn(feed), FadeIn(glucose), run_time=0.7)
        self.at("It releases oxygen")
        self.play(FadeIn(oxygen), run_time=0.6)
        self.at("Respiration breaks")
        top = VMobject(color=GREY, stroke_width=4).set_points_as_corners([
            [-3.9, 1.7, 0], [-3.9, 2.7, 0], [-2.1, 2.7, 0]])
        into_resp = arrow([2.6, 2.7, 0], [3.9, 1.7, 0], GREY)
        self.play(FadeIn(resp), Create(top), GrowArrow(into_resp), run_time=0.7)
        return1 = arrow([3.9, 0.5, 0], [2.2, -0.4, 0], GREY)
        return2 = arrow([-2.5, -0.4, 0], [-3.9, 0.5, 0], GREY)
        self.at("into carbon dioxide")
        self.play(GrowArrow(return1), GrowArrow(return2), run_time=0.7)
        self.at("Plants do both")
        plant = lab("Plants do both", [0, 1.1, 0], TEXT, 30, BOLD)
        self.play(FadeIn(plant), run_time=0.5)
        self.at("The atoms go")
        self.play(Indicate(glucose, color=YELLOW), Indicate(oxygen, color=BLUE), run_time=0.6)
        # Move the existing labels, keeping every label distinct throughout the loop.
        matter = VGroup(glucose, oxygen)
        matter_home, feed_home = matter.get_center().copy(), feed.get_center().copy()
        self.play(matter.animate.move_to([3.9, 2.7, 0]),
                  feed.animate.move_to([-3.9, -0.4, 0]), run_time=0.65)
        self.play(FadeOut(matter), FadeOut(feed), run_time=0.2)
        matter.move_to(matter_home)
        feed.move_to(feed_home)
        self.play(FadeIn(matter), FadeIn(feed), run_time=0.3)
        self.at("Energy arrives")
        self.play(FadeOut(light), FadeOut(incoming), run_time=0.2)
        energy_path = VGroup(*[lab(t, [x, -2.3, 0], c, 28, BOLD) for t, x, c in
            [("light", -5.4, GOLD), ("food", -2.8, YELLOW), ("ATP", 0, GREEN),
             ("cell work", 2.8, TEXT), ("heat", 5.5, GOLD)]])
        arrows = VGroup(*[arrow([a, -2.3, 0], [b, -2.3, 0], GOLD) for a, b in
                         [(-4.9, -3.5), (-2.2, -0.7), (0.7, 1.8), (3.8, 4.9)]])
        self.play(FadeIn(energy_path[0]), FadeIn(energy_path[4]), run_time=0.5)
        self.at("Along the way")
        self.play(FadeIn(VGroup(*energy_path[1:4])),
                  LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2), run_time=1.1)
        energy_l = lab("energy flows through", [0, -3.2, 0], GOLD, 26)
        self.play(FadeIn(energy_l), run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "ATP carries energy; respiration or fermentation rebuilds it."
