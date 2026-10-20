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


class S00Title(TitleCard):
    LESSON = "Respiration and ATP"
    TITLE = "Food Energy Becomes ATP"


# ---------------------------------------------------------------------------------------------
class S01Question(SpokenScene):
    def construct(self):
        xs = [-4.5, 0, 4.5]
        cards = []
        for x in xs:
            r = RoundedRectangle(corner_radius=0.2, width=4.0, height=4.6, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.08).move_to([x, 0.1, 0])
            cards.append(r)
        # icons
        leg = RoundedRectangle(corner_radius=0.3, width=2.6, height=1.5, stroke_color=RED, stroke_width=5,
                               fill_color=RED, fill_opacity=0.2).move_to([xs[0], 1.1, 0])
        leg_t = T("leg muscle", 26, TEXT).move_to(leg)
        dough = Ellipse(width=2.8, height=1.5, stroke_color=YELLOW, stroke_width=4, fill_color=YELLOW,
                        fill_opacity=0.2).move_to([xs[1], 1.1, 0])
        bubbles = VGroup(*[Circle(radius=r, stroke_color=TEXT, stroke_width=3).move_to([xs[1] + dx, 1.1 + dy, 0])
                           for r, dx, dy in [(0.17, -0.7, 0.1), (0.25, 0.1, 0.2), (0.14, 0.7, -0.1), (0.2, -0.2, -0.3)]])
        bay = Rectangle(width=2.8, height=1.5, stroke_color=TEAL, stroke_width=4, fill_color=TEAL,
                        fill_opacity=0.25).move_to([xs[2], 1.1, 0])
        bay_t = T("deep water", 26, TEXT).move_to(bay)
        t1 = VGroup(T("Legs burn", 30, TEXT, weight=BOLD), T("after a sprint", 26, GREY)).arrange(DOWN, buff=0.12).move_to([xs[0], -1.2, 0])
        t2 = VGroup(T("Dough", 30, TEXT, weight=BOLD), T("puffs up", 26, GREY)).arrange(DOWN, buff=0.12).move_to([xs[1], -1.2, 0])
        t3 = VGroup(T("Deep Bay, summer", 30, TEXT, weight=BOLD), T("parts hold very", 24, GREY), T("little oxygen", 24, GREY)).arrange(DOWN, buff=0.08).move_to([xs[2], -1.3, 0])
        g1, g2, g3 = VGroup(cards[0], leg, leg_t, t1), VGroup(cards[1], dough, bubbles, t2), VGroup(cards[2], bay, bay_t, t3)
        self.at("your legs may burn")
        self.play(FadeIn(g1, shift=UP * 0.2), run_time=0.7)
        self.play(leg.animate.set_fill(RED, 0.55), rate_func=there_and_back, run_time=0.8)
        self.at("Bread dough puffs")
        self.play(FadeIn(g2, shift=UP * 0.2), run_time=0.7)
        self.play(bubbles.animate.shift(UP * 0.12).scale(1.25), rate_func=there_and_back, run_time=0.8)
        self.at("deep Chesapeake Bay")
        self.play(FadeIn(g3, shift=UP * 0.2), run_time=0.7)
        self.at("All three are about")
        self.play(FadeOut(VGroup(g1, g2, g3)), run_time=0.6)
        q = VGroup(T("How does the energy in food", 46, TEXT, weight=BOLD),
                   T("become energy a cell can use,", 46, TEXT, weight=BOLD),
                   T("with or without oxygen?", 46, BLUE, weight=BOLD)).arrange(DOWN, buff=0.3)
        self.at("How does the energy")
        self.play(FadeIn(q[0], shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(q[1], shift=UP * 0.15), run_time=0.6)
        self.at("with or without oxygen")
        self.play(FadeIn(q[2], shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Respire(SpokenScene):
    def construct(self):
        cell = RoundedRectangle(corner_radius=0.6, width=11.6, height=5.0, stroke_color=GREY, stroke_width=4).move_to([0.2, 0.0, 0])
        cyt = lab("cytoplasm", [-3.6, -2.05, 0], GREY, 26)
        title = T("cellular respiration", 38, TEXT, weight=BOLD).move_to([0, 3.15, 0])
        gluc = chip("glucose", YELLOW, 30).move_to([-4.4, 1.3, 0])
        first = lab("first steps", [-4.4, -0.55, 0], GREY, 26)
        mito = RoundedRectangle(corner_radius=0.9, width=5.2, height=3.6, stroke_color=PINK, stroke_width=5,
                                fill_color=PINK, fill_opacity=0.1).move_to([2.8, -0.2, 0])
        mito_l = lab("mitochondria", [2.8, 1.15, 0], PINK, 28, BOLD)
        oxy = chip("oxygen", BLUE, 28).move_to([2.0, 3.0 - 6.0, 0])
        orgs = lab("organelles in plant, animal and fungal cells", [0, -2.95, 0], GREY, 24)
        self.at("break down glucose")
        self.play(Create(cell), FadeIn(cyt), FadeIn(gluc, shift=RIGHT * 0.3), run_time=0.9)
        self.at("called cellular respiration")
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.5)
        self.at("first steps")
        self.play(gluc.animate.move_to([-4.4, 0.3, 0]), FadeIn(first), run_time=0.7)
        self.at("mitochondria")
        self.play(Create(mito), FadeIn(mito_l), run_time=0.7)
        self.at("organelles in plant")
        self.play(FadeIn(orgs), run_time=0.5)
        self.at("With oxygen")
        oxy.move_to([-1.0, -1.9, 0])
        later = lab("later steps", [3.9, -0.45, 0], PINK, 26)
        self.play(FadeOut(orgs), FadeIn(oxy, shift=UP * 0.3), run_time=0.4)
        self.play(oxy.animate.move_to([1.7, -0.45, 0]), FadeIn(later), run_time=0.7)
        self.at("glucose becomes")
        e_o = lab("overall:", [-5.2, -3.2, 0], GREY, 24)
        e_g = chip("glucose", YELLOW, 22)
        e_p1 = T("+", 28, TEXT)
        e_x = chip("oxygen", BLUE, 22)
        e_a = Arrow(LEFT * 0.3, RIGHT * 0.3, color=TEXT, stroke_width=5, buff=0)
        e_c = chip("carbon dioxide", GREY, 22)
        e_p2 = T("+", 28, TEXT)
        e_w = chip("water", TEAL, 22)
        eq = VGroup(e_g, e_p1, e_x, e_a, e_c, e_p2, e_w).arrange(RIGHT, buff=0.2).move_to([0.6, -3.2, 0])
        e_o.next_to(eq, LEFT, buff=0.3)
        self.play(FadeIn(e_o), FadeIn(VGroup(e_g, e_p1, e_x, e_a)), run_time=0.8)
        self.at("carbon dioxide and water")
        self.play(FadeIn(VGroup(e_c, e_p2, e_w), shift=RIGHT * 0.2), run_time=0.8)
        self.at("released energy")
        atp = chip("ATP", GREEN, 34).move_to([-1.2, -0.2, 0])
        arr = Arrow([0.2, -0.2, 0], [-0.45, -0.2, 0], color=GOLD, stroke_width=6, buff=0)
        cap = lab("energy captured", [-1.2, -1.05, 0], GOLD, 24)
        self.play(GrowArrow(arr), FadeIn(atp, shift=LEFT * 0.3), FadeIn(cap), run_time=0.8)
        self.at("small molecule called")
        self.play(Indicate(atp, color=GREEN, scale_factor=1.2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Atp(SpokenScene):
    def construct(self):
        y = 0.9
        ade = base_block("adenosine", GREEN, [-3.9, y], 2.6, 1.2)
        ps = [psq([-1.9 + i * 1.0, y]) for i in range(3)]
        atp_l = T("ATP", 52, GREEN, weight=BOLD).move_to([-3.9, 2.2, 0])
        pl = lab("three phosphate groups", [-0.9, 0.0, 0], PURPLE, 26)
        self.at("three phosphate groups")
        self.play(FadeIn(ade), FadeIn(atp_l), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.2) for p in ps], lag_ratio=0.35), FadeIn(pl), run_time=1.2)
        self.at("added or removed")
        self.play(Indicate(ps[2], color=PURPLE, scale_factor=1.2), run_time=0.8)
        self.at("reacts with water")
        w = chip("water", TEAL, 28).move_to([3.5, 2.4, 0])
        self.play(FadeIn(w, shift=DOWN * 0.2), run_time=0.4)
        self.play(w.animate.move_to([1.1, 2.0, 0]), run_time=0.7)
        self.at("comes off")
        pl2 = lab("phosphate", [3.9, -0.4, 0], PURPLE, 26)
        self.play(FadeOut(w), ps[2].animate.move_to([3.9, 0.5, 0]), FadeIn(pl2), FadeOut(pl), run_time=0.9)
        self.at("What is left")
        adp_l = T("ADP", 52, ORANGE, weight=BOLD).move_to([-3.9, 2.2, 0])
        pl3 = lab("two phosphate groups", [-1.4, 0.0, 0], PURPLE, 26)
        self.play(Transform(atp_l, adp_l), ade[0].animate.set_stroke(ORANGE).set_fill(ORANGE, 0.2),
                  FadeIn(pl3), run_time=0.8)
        self.at("releases energy")
        work = chip("cell work", TEXT, 30).move_to([-3.9, -2.0, 0])
        en = Arrow([1.0, 0.3, 0], [-2.6, -1.8, 0], color=GOLD, stroke_width=7, buff=0)
        en_l = lab("energy", [0.9, -0.75, 0], GOLD, 28, BOLD)
        self.play(GrowArrow(en), FadeIn(en_l), FadeIn(work), run_time=0.8)
        self.at("is not energy")
        n1 = T("ATP is not energy.", 40, TEXT, weight=BOLD).move_to([2.0, -1.9, 0])
        self.play(FadeIn(n1, shift=UP * 0.15), run_time=0.5)
        self.at("carries energy")
        n2 = T("It is a molecule that carries energy.", 30, GREEN).move_to([2.0, -2.65, 0])
        self.play(FadeIn(n2, shift=UP * 0.15), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Cycle(SpokenScene):
    def construct(self):
        atp = chip("ATP", GREEN, 44).move_to([-4.4, 0.4, 0])
        adp = chip("ADP + phosphate", ORANGE, 34).move_to([4.0, 0.4, 0])
        top = Arrow([-2.7, 1.0, 0], [1.6, 1.0, 0], color=TEXT, stroke_width=6, buff=0)
        bot = Arrow([1.6, -0.2, 0], [-2.7, -0.2, 0], color=GOLD, stroke_width=8, buff=0)
        bot_l = lab("cellular respiration", [-0.5, -0.95, 0], GOLD, 30, BOLD)
        top_l = lab("cell work", [-0.5, 1.65, 0], TEXT, 32, BOLD)
        en = lab("adds energy", [-0.5, -1.55, 0], GOLD, 26)
        self.at("Putting a phosphate")
        self.play(FadeIn(atp), FadeIn(adp), run_time=0.6)
        self.at("takes energy")
        self.play(GrowArrow(bot), FadeIn(en), run_time=0.7)
        self.at("Cellular respiration supplies")
        self.play(FadeIn(bot_l), run_time=0.4)
        dot = Dot(color=YELLOW, radius=0.14).move_to([1.6, -0.2, 0])
        self.at("go round in a cycle")
        self.play(GrowArrow(top), run_time=0.6)
        self.add(dot)
        path = VMobject().set_points_as_corners([[1.6, -0.2, 0], [-2.7, -0.2, 0], [-2.7, 1.0, 0], [1.6, 1.0, 0], [1.6, -0.2, 0]])
        self.play(MoveAlongPath(dot, path), run_time=1.1, rate_func=linear)
        self.at("Cell work turns")
        self.play(FadeIn(top_l), run_time=0.4)
        self.at("small supply")
        supply = VGroup(*[RoundedRectangle(corner_radius=0.08, width=0.8, height=0.5, stroke_color=GREEN, stroke_width=3,
                                           fill_color=GREEN, fill_opacity=0.3) for _ in range(3)]).arrange(RIGHT, buff=0.12)
        supply.move_to([-4.4, -2.1, 0])
        sup_l = lab("a small supply of ATP", [-3.9, -2.9, 0], GREEN, 26)
        self.play(FadeIn(supply), FadeIn(sup_l), run_time=0.6)
        self.at("all the time")
        self.play(MoveAlongPath(dot, path), run_time=1.6, rate_func=linear)
        self.play(MoveAlongPath(dot, path), run_time=1.6, rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Ferment(SpokenScene):
    def construct(self):
        v1 = VGroup(T("aerobic", 38, TEXT, weight=BOLD), T("uses oxygen", 28, BLUE)).arrange(DOWN, buff=0.2).move_to([-3.4, 3.0, 0])
        v2 = VGroup(T("anaerobic", 38, TEXT, weight=BOLD), T("without oxygen", 28, BLUE)).arrange(DOWN, buff=0.2).move_to([3.4, 3.0, 0])
        gluc = chip("glucose", YELLOW, 28).move_to([-5.6, -0.2, 0])
        oxy = chip("oxygen", BLUE, 26).move_to([-5.6, 1.3, 0])
        cross = VGroup(Line(oxy.get_corner(UL), oxy.get_corner(DR), color=RED, stroke_width=7),
                       Line(oxy.get_corner(DL), oxy.get_corner(UR), color=RED, stroke_width=7))
        box = RoundedRectangle(corner_radius=0.2, width=3.2, height=1.6, stroke_color=GREY, stroke_width=4).move_to([-2.2, -0.2, 0])
        box_l = T("fermentation", 30, TEXT, weight=BOLD).move_to(box)
        a1 = Arrow([-4.55, -0.2, 0], [-3.85, -0.2, 0], color=TEXT, stroke_width=5, buff=0)
        atp = chip("a little ATP", GREEN, 26).move_to([-2.2, -1.95, 0])
        a2 = Arrow([-2.2, -1.0, 0], [-2.2, -1.55, 0], color=GREEN, stroke_width=5, buff=0)
        sol = lab("SOL name: anaerobic respiration", [-2.2, -2.9, 0], GOLD, 24)
        mus = lab("in muscle", [2.6, 2.0, 0], GREY, 26)
        lac = chip("lactate", RED, 28).move_to([2.6, 1.3, 0])
        a3 = Arrow([-0.5, 0.1, 0], [1.3, 1.1, 0], color=TEXT, stroke_width=5, buff=0)
        yea = lab("in yeast", [2.6, 0.0, 0], GREY, 26)
        eth = chip("ethanol", RED, 28).move_to([2.6, -0.8, 0])
        co2 = chip("carbon dioxide", GREY, 26).move_to([2.6, -1.8, 0])
        a4 = Arrow([-0.5, -0.5, 0], [1.2, -1.4, 0], color=TEXT, stroke_width=5, buff=0)
        bub = VGroup(*[Circle(radius=r, stroke_color=TEXT, stroke_width=3).move_to([5.3 + dx, -1.5 + dy, 0])
                       for r, dx, dy in [(0.2, -0.3, -0.5), (0.3, 0.2, 0.0), (0.15, -0.2, 0.6), (0.22, 0.4, 0.8)]])
        dr = lab("dough rises", [5.3, -2.7, 0], TEXT, 26)
        self.at("Aerobic means")
        self.play(FadeIn(v1, shift=DOWN * 0.15), run_time=0.5)
        self.at("Anaerobic means")
        self.play(FadeIn(v2, shift=DOWN * 0.15), run_time=0.5)
        self.at("Without oxygen")
        self.play(FadeIn(oxy), FadeIn(gluc), run_time=0.5)
        self.play(Create(cross), run_time=0.5)
        self.at("muscle cells and yeast")
        self.play(FadeIn(a1), Create(box), FadeIn(box_l), run_time=0.7)
        self.at("small amount")
        self.play(GrowArrow(a2), FadeIn(atp), run_time=0.6)
        self.at("calls this")
        self.play(FadeIn(sol), run_time=0.5)
        self.at("In muscle")
        self.play(GrowArrow(a3), FadeIn(mus), FadeIn(lac), run_time=0.7)
        self.at("In yeast")
        self.play(GrowArrow(a4), FadeIn(yea), FadeIn(eth), FadeIn(co2), run_time=0.8)
        self.at("forms the bubbles")
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in bub], lag_ratio=0.2), run_time=0.8)
        self.at("make dough rise")
        self.play(FadeIn(dr), bub.animate.shift(UP * 0.3), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        base_y, k = -2.4, 0.1
        axis = Line([-6.2, base_y, 0], [-1.0, base_y, 0], color=GREY, stroke_width=3)
        yl = lab("ATP per glucose", [-3.6, 2.9, 0], GREY, 28)
        b1 = Rectangle(width=1.6, height=31 * k, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.4)
        b1.move_to([-4.8, base_y + 31 * k / 2, 0])
        b2 = Rectangle(width=1.6, height=2 * k, stroke_color=RED, stroke_width=3, fill_color=RED, fill_opacity=0.5)
        b2.move_to([-2.4, base_y + 2 * k / 2, 0])
        l1 = lab("with oxygen", [-4.8, base_y - 0.4, 0], TEXT, 24)
        l2 = lab("fermentation", [-2.4, base_y - 0.4, 0], TEXT, 24)
        v1 = lab("about 30 to 32", [-4.8, base_y + 31 * k + 0.4, 0], GREEN, 28, BOLD)
        v2 = lab("2", [-2.4, base_y + 0.65, 0], RED, 36, BOLD)
        sp1 = T("One 2024 estimate: fermentation", 28, YELLOW, weight=BOLD)
        sp2 = T("makes ATP faster for the same amount", 24, TEXT)
        sp3 = T("of enzyme, in yeast and mammal cells", 24, GREY)
        speed = VGroup(sp1, sp2, sp3).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([3.5, 2.3, 0])
        use = Arrow([1.0, 0.2, 0], [5.8, 0.2, 0], color=GOLD, stroke_width=8, buff=0)
        use_l = lab("ATP used by muscles in a sprint", [3.4, 0.75, 0], GOLD, 24)
        reb = Arrow([1.0, -0.7, 0], [3.8, -0.7, 0], color=GREEN, stroke_width=8, buff=0)
        reb_l = lab("rebuilt by aerobic respiration alone", [3.4, -1.25, 0], GREEN, 24)
        add = Arrow([3.9, -0.7, 0], [5.8, -0.7, 0], color=RED, stroke_width=8, buff=0)
        add_l = lab("added by fermentation", [3.4, -1.75, 0], RED, 24)
        sk = lab("in this sketch, lengths not to scale", [3.4, -2.4, 0], TEXT, 24)
        ans = VGroup(T("Food energy reaches", 34, TEXT, weight=BOLD), T("cell work through ATP,", 34, GREEN, weight=BOLD),
                     T("rebuilt with oxygen", 34, BLUE, weight=BOLD), T("or without it.", 34, RED, weight=BOLD)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.4, 0.0, 0])
        self.at("With oxygen")
        self.play(Create(axis), FadeIn(yl), FadeIn(l1), FadeIn(l2), run_time=0.5)
        self.play(GrowFromEdge(b1, DOWN), run_time=1.2)
        self.play(FadeIn(v1), run_time=0.3)
        self.at("Fermentation gives")
        self.play(GrowFromEdge(b2, DOWN), FadeIn(v2), run_time=0.7)
        self.at("faster for the same")
        self.play(FadeIn(speed, shift=LEFT * 0.2), run_time=0.6)
        self.at("In a sprint")
        self.play(FadeIn(use), FadeIn(use_l), run_time=0.7)
        self.play(GrowArrow(reb), FadeIn(reb_l), FadeIn(sk), run_time=0.7)
        self.at("So fermentation adds")
        self.play(GrowArrow(add), FadeIn(add_l), run_time=0.7)
        self.at("Food energy reaches")
        self.play(FadeOut(VGroup(speed, use, use_l, reb, reb_l, add, add_l, sk)), run_time=0.5)
        self.play(FadeIn(ans, shift=UP * 0.15), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "ATP carries energy; respiration or fermentation rebuilds it."
