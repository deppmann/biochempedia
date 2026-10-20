"""Matter cycles: atoms move, and no cycle runs alone  (Biochemistrypedia high school Biology explainer)

COLOR MAP (one color per concept, whole video)
  YELLOW = carbon (the C token, carbon dioxide, sugar)
  GREEN  = nitrogen (the N token, nitrogen gas, ammonia, nitrate)
  BLUE   = water (vapor, rain, river, Bay, ocean)
  ORANGE = living things (crab, plant, animal, dead organisms)
  PURPLE = microbes (bacteria, fungi, decomposers)
  RED    = what people do (burning) and a blocked path
  GOLD   = light energy
  GREY   = air, ground, outlines, labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    """chip with an opaque backing so lines behind it do not show through."""
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def recolor_chip(c, color):
    return [c[1].animate.set_stroke(color).set_fill(color, 0.16), c[2].animate.set_color(color)]


def btext(text, size=24, color=GREY):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.2, height=t.height + 0.14, stroke_width=0, fill_color=BG,
                     fill_opacity=1).move_to(t)
    return VGroup(back, t)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def token(letter, color, r=0.27):
    sq = RoundedRectangle(corner_radius=0.09, width=2 * r, height=2 * r, stroke_color=color, stroke_width=3,
                          fill_color=color, fill_opacity=1)
    return VGroup(sq, T(letter, 24, BG, weight=BOLD).move_to(sq))


def up(n):
    return np.array([n[0], n[1], 0.0])


def P(x, y):
    return np.array([x, y, 0.0])


def riding(tok, a, b, rt=1.0):
    """slide a token from a to b."""
    return tok.animate.move_to(b)


class S00Title(TitleCard):
    LESSON = "Matter cycles"
    TITLE = "Atoms Move, and No Cycle Runs Alone"


# ---------------------------------------------------------------------------------------------
class S01Crab(SpokenScene):
    """a crab block, question-mark sources, tokens ride in, then the two questions."""

    def construct(self):
        crab = bchip("blue crab", ORANGE, 58, pad=0.45).move_to(P(0, 0.9))
        bay = T("Chesapeake Bay", 32, GREY).next_to(crab, DOWN, buff=0.25)
        self.at("blue crab")
        self.play(FadeIn(crab, scale=0.9), run_time=0.7)
        self.at("Chesapeake Bay")
        self.play(FadeIn(bay), run_time=0.4)

        spots = [P(-4.9, 2.2), P(-4.9, -0.7), P(4.9, 2.2), P(4.9, -0.7)]
        boxes, arrows = [], []
        for s in spots:
            b = RoundedRectangle(corner_radius=0.14, width=1.9, height=1.6, stroke_color=GREY, stroke_width=3,
                                 fill_color=GREY, fill_opacity=0.12).move_to(s)
            q = T("?", 64, GREY, weight=BOLD).move_to(b)
            side = RIGHT if s[0] < 0 else LEFT
            tgt = crab.get_center() + P(-side[0] * 0 + (-1) * side[0] * 0, 0)
            end = P(crab.get_edge_center(-side)[0], 0.9 + (0.45 if s[1] > 0 else -0.35))
            a = arr(P(b.get_edge_center(side)[0], s[1], ), end, GREY, 6)
            boxes.append(VGroup(b, q))
            arrows.append(a)
        self.at("somewhere else before")
        self.play(*[FadeIn(b, scale=0.9) for b in boxes], run_time=0.7)
        self.at("one particular crab")
        self.play(crab.animate.scale(1.06), rate_func=there_and_back, run_time=0.8)
        self.at("trace the routes")
        self.play(*[GrowArrow(a) for a in arrows], run_time=0.6)
        toks = []
        for i, s in enumerate(spots):
            t = token("C" if i % 2 == 0 else "N", YELLOW if i % 2 == 0 else GREEN).move_to(
                arrows[i].get_start() + (RIGHT if s[0] < 0 else LEFT) * 0.2)
            toks.append(t)
        self.play(*[FadeIn(t) for t in toks], run_time=0.3)
        self.play(*[t.animate.move_to(a.get_end()) for t, a in zip(toks, arrows)], run_time=1.6)
        self.play(*[FadeOut(t) for t in toks], run_time=0.4)
        q1 = T("How does matter keep moving through ecosystems?", 34, TEXT).move_to(P(0, -2.45))
        self.at("How does matter keep moving")
        self.play(FadeIn(q1, shift=UP * 0.1), run_time=0.5)
        q2 = T("What happens when people change a cycle?", 34, RED).move_to(P(0, -3.2))
        self.at("when people change a cycle")
        self.play(FadeIn(q2, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
def carbon_base():
    return bchip("carbon dioxide in air", GREY, 38).move_to(P(0, 2.7))


class S02Carbon(SpokenScene):
    """carbon in sugar, fat, protein -> photosynthesis pulls it into a plant -> respiration returns it."""

    def construct(self):
        hd = T("carbon", 56, YELLOW, weight=BOLD).move_to(P(0, 2.4))
        chips = VGroup(*[VGroup(bchip(n, YELLOW, 38), token("C", YELLOW, 0.33)).arrange(RIGHT, buff=0.2)
                         for n in ["sugar", "fat", "protein"]]).arrange(RIGHT, buff=0.55).move_to(P(0, 0.2))
        self.at("Carbon is in every sugar")
        self.play(FadeIn(hd), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in chips], lag_ratio=0.35), run_time=1.6)
        body = T("in your body", 34, GREY).next_to(chips, DOWN, buff=0.5)
        self.at("your body")
        self.play(FadeIn(body), run_time=0.4)

        air = carbon_base()
        plant = bchip("plant or alga", ORANGE, 34).move_to(P(-4.5, -1.5))
        self.at("Photosynthesis")
        self.play(FadeOut(chips), FadeOut(body), FadeOut(hd), FadeIn(air), FadeIn(plant), run_time=0.8)
        down = arr(P(-2.4, 2.1), P(-4.8, -0.95), YELLOW, 7)
        lab = T("photosynthesis", 30, TEXT).move_to(P(-4.85, 1.2))
        ct = token("C", YELLOW, 0.33).move_to(P(-2.4, 2.1))
        self.play(GrowArrow(down), FadeIn(lab), FadeIn(ct), run_time=0.7)
        light = T("light energy", 28, GOLD).next_to(lab, DOWN, buff=0.15)
        self.at("light energy")
        self.play(FadeIn(light), run_time=0.4)
        sugar = bchip("sugar", YELLOW, 34).move_to(P(-4.5, -3.0))
        self.at("build sugar")
        self.play(ct.animate.move_to(P(-4.8, -0.95)), run_time=0.8)
        self.play(FadeOut(ct), FadeIn(sugar, shift=UP * 0.1), run_time=0.5)
        self.at("carbon dioxide and water")
        self.play(air.animate.scale(1.08), rate_func=there_and_back, run_time=0.8)

        upa = arr(P(-4.0, -0.95), P(-1.6, 2.1), YELLOW, 7)
        rlab = T("respiration", 30, TEXT).move_to(P(-1.2, 0.3))
        c2 = token("C", YELLOW, 0.33).move_to(sugar.get_center() + UP * 0.0)
        self.at("Respiration")
        self.play(GrowArrow(upa), FadeIn(rlab), run_time=0.7)
        self.at("break down sugar")
        self.play(sugar.animate.scale(1.12), rate_func=there_and_back, run_time=0.6)
        self.play(FadeIn(c2.move_to(sugar.get_right() + RIGHT * 0.4)), run_time=0.2)
        self.play(c2.animate.move_to(P(-3.85, -0.6)), FadeOut(sugar), run_time=0.6)
        self.at("release carbon dioxide")
        self.play(c2.animate.move_to(P(-1.6, 2.1)), run_time=0.9)
        self.play(FadeOut(c2), run_time=0.2)

        animal = bchip("animal", ORANGE, 34).move_to(P(0.7, -1.5))
        micro = bchip("microbes", PURPLE, 34).move_to(P(4.7, -1.5))
        a2 = arr(P(0.7, -0.95), P(0.7, 2.05), YELLOW, 7)
        a3 = arr(P(4.4, -0.95), P(1.9, 2.1), YELLOW, 7)
        self.at("Plants, animals and microbes")
        self.play(FadeIn(animal, shift=UP * 0.1), FadeIn(micro, shift=UP * 0.1), run_time=0.7)
        self.at("all do it")
        t1 = token("C", YELLOW, 0.33).move_to(P(0.7, -0.95))
        t2 = token("C", YELLOW, 0.33).move_to(P(4.4, -0.95))
        self.play(GrowArrow(a2), GrowArrow(a3), FadeIn(t1), FadeIn(t2), run_time=0.6)
        self.play(t1.animate.move_to(P(0.7, 2.05)), t2.animate.move_to(P(1.9, 2.1)), run_time=1.0)
        self.play(FadeOut(t1), FadeOut(t2), run_time=0.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03More(SpokenScene):
    """combustion, decomposition, ocean absorption, all against the same air box."""

    def construct(self):
        air = carbon_base()
        self.add(air)
        burn = bchip("burning", RED, 34).move_to(P(-4.8, -1.5))
        a1 = arr(P(-4.8, -0.95), P(-2.4, 2.1), RED, 10)
        l1 = T("combustion", 30, TEXT).move_to(P(-5.0, 0.9))
        self.at("Combustion")
        self.play(FadeIn(burn, shift=UP * 0.1), run_time=0.5)
        self.at("releases carbon dioxide quickly")
        t = token("C", YELLOW, 0.33).move_to(P(-4.8, -0.95))
        self.play(GrowArrow(a1), FadeIn(l1), FadeIn(t), run_time=0.5)
        self.play(t.animate.move_to(P(-2.4, 2.1)), run_time=0.6)
        self.play(FadeOut(t), run_time=0.2)

        dead = bchip("dead organisms", ORANGE, 34).move_to(P(-0.1, -1.5))
        fb = bchip("fungi and bacteria", PURPLE, 30).move_to(P(-0.1, -2.9))
        a2 = arr(P(-0.1, -0.95), P(-0.1, 2.05), YELLOW, 7)
        l2 = T("decomposition", 30, TEXT).move_to(P(1.45, 0.6))
        self.at("Decomposition")
        self.play(FadeIn(dead, shift=UP * 0.1), run_time=0.5)
        self.at("by fungi and bacteria")
        self.play(FadeIn(fb, shift=UP * 0.1), run_time=0.5)
        self.at("Their respiration")
        t2 = token("C", YELLOW, 0.33).move_to(P(-0.1, -0.95))
        self.play(GrowArrow(a2), FadeIn(l2), FadeIn(t2), run_time=0.5)
        self.play(t2.animate.move_to(P(-0.1, 2.05)), run_time=0.8)
        self.play(FadeOut(t2), run_time=0.2)

        ocean = bchip("ocean", BLUE, 34).move_to(P(5.0, -1.5))
        l3 = T("ocean absorption", 28, TEXT).move_to(P(4.5, -2.6))
        self.at("Ocean absorption")
        self.play(FadeIn(ocean, shift=UP * 0.1), FadeIn(l3), run_time=0.5)
        self.at("dissolving into seawater")
        t3 = token("C", YELLOW, 0.33).move_to(P(2.2, 2.1))
        a3 = arr(P(2.2, 2.1), P(4.3, -0.95), YELLOW, 7)
        self.play(GrowArrow(a3), FadeIn(t3), run_time=0.5)
        self.play(t3.animate.move_to(P(4.3, -0.95)), run_time=0.8)
        self.play(FadeOut(t3), run_time=0.2)
        a4 = arr(P(5.7, -0.95), P(3.3, 2.1), YELLOW, 3)
        t4 = token("C", YELLOW, 0.33).move_to(P(5.7, -0.95))
        self.at("also comes back out")
        self.play(GrowArrow(a4), FadeIn(t4), run_time=0.4)
        self.play(t4.animate.move_to(P(3.3, 2.1)), run_time=0.8)
        self.play(FadeOut(t4), run_time=0.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Water(SpokenScene):
    """evaporation, condensation, precipitation, then runoff carries nitrogen, sediment, germs to the Bay."""

    def construct(self):
        bay = bchip("liquid water", BLUE, 34).move_to(P(-4.5, -2.5))
        cloud = bchip("water vapor", BLUE, 34).move_to(P(-4.5, 2.6))
        farm = bchip("farm in Pennsylvania", ORANGE, 30).move_to(P(4.0, 1.0))
        ev = arr(P(-4.5, -1.95), P(-4.5, 2.0), BLUE, 7)
        evl = T("evaporation", 30, TEXT).move_to(P(-2.75, 0.2))
        self.at("Water cycles too")
        self.play(FadeIn(bay, shift=UP * 0.1), run_time=0.5)
        self.at("Evaporation")
        self.play(GrowArrow(ev), FadeIn(evl), FadeIn(cloud, shift=UP * 0.2), run_time=0.9)
        drops = bchip("cloud droplets", BLUE, 34).move_to(P(0.5, 2.6))
        cond = arr(P(-2.5, 2.6), P(-1.45, 2.6), BLUE, 7)
        condl = T("condensation", 30, TEXT).move_to(P(-2.0, 1.85))
        self.at("Condensation")
        self.play(GrowArrow(cond), FadeIn(condl), FadeIn(drops, shift=RIGHT * 0.2), run_time=0.9)
        pr = arr(P(1.5, 2.1), P(3.0, 1.55), BLUE, 7)
        prl = T("precipitation:\nrain or snow", 28, TEXT, line_spacing=0.8).move_to(P(4.6, 2.55))
        self.at("Precipitation")
        self.play(FadeIn(farm, shift=DOWN * 0.1), GrowArrow(pr), FadeIn(prl), run_time=0.9)

        riv_y = -2.5
        river_v = Line(P(4.0, 0.5), P(4.0, riv_y), color=BLUE, stroke_width=14).set_stroke(opacity=0.5)
        river_h = Line(P(4.0, riv_y), P(-2.2, riv_y), color=BLUE, stroke_width=14).set_stroke(opacity=0.5)
        rl = T("Susquehanna River", 30, TEXT).move_to(P(1.0, riv_y + 0.95))
        toks = [bchip("nitrogen", GREEN, 28), bchip("sediment", GREY, 28), bchip("germs", PURPLE, 28)]
        ys = [-0.05, -0.95, -1.85]
        self.at("Moving water carries")
        self.play(Create(river_v), run_time=0.5)
        self.at("nutrients such as nitrogen")
        toks[0].move_to(P(4.0, ys[0]))
        self.play(FadeIn(toks[0]), run_time=0.3)
        self.at("sediment")
        toks[1].move_to(P(4.0, ys[1]))
        self.play(FadeIn(toks[1]), run_time=0.3)
        self.at("and germs")
        toks[2].move_to(P(4.0, ys[2]))
        self.play(FadeIn(toks[2]), run_time=0.3)
        self.at("rainstorm in Pennsylvania")
        self.play(Create(river_h), FadeIn(rl), run_time=0.5)
        self.at("Susquehanna River")
        ends = [P(-0.9, riv_y), P(1.3, riv_y), P(3.15, riv_y)]
        paths = []
        for i, t in enumerate(toks):
            pth = VMobject().set_points_as_corners([t.get_center(), P(4.0, riv_y + 0.0) if i < 2 else P(4.0, riv_y), ends[i]])
            paths.append(pth)
        # nitrogen leads along the bend; sediment and germs follow
        self.play(*[MoveAlongPath(t, p) for t, p in zip(toks, paths)], run_time=1.4)
        bay2 = bchip("Chesapeake Bay", BLUE, 34).move_to(bay)
        self.at("flows into the Bay")
        self.play(Transform(bay, bay2), FadeOut(ev), FadeOut(evl), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Nitrogen(SpokenScene):
    """the nitrogen cycle: gas, ammonia, nitrate, living things, ammonium."""

    def construct(self):
        living = bchip("plants and other living things", ORANGE, 32).move_to(P(0, -2.6))
        gas = bchip("nitrogen gas", GREEN, 38).move_to(P(-3.8, 2.5))
        pct = T("about 78 percent of air", 28, GREY).next_to(gas, DOWN, buff=0.2)
        bond = bchip("very strong bond", RED, 28).next_to(pct, DOWN, buff=0.25)
        self.at("Your body uses nitrogen")
        self.play(FadeIn(living, shift=UP * 0.1), run_time=0.6)
        self.at("Air is about")
        self.play(FadeIn(gas, shift=DOWN * 0.1), FadeIn(pct), run_time=0.7)
        self.at("held by a very strong bond")
        self.play(FadeIn(bond, shift=UP * 0.1), run_time=0.5)
        block = arr(P(-3.6, 0.15), P(-1.6, -2.0), RED, 7)
        x = T("X", 64, RED, weight=BOLD).move_to(P(-2.6, -0.9))
        bl = T("most organisms cannot use it", 28, RED).move_to(P(1.1, -0.8))
        self.at("Most organisms cannot break it")
        self.play(GrowArrow(block), FadeIn(x), FadeIn(bl), run_time=0.7)

        ammonia = bchip("ammonia", GREEN, 38).move_to(P(3.8, 2.5))
        fix = arr(P(-1.6, 2.5), P(2.3, 2.5), GREEN, 7)
        fl = T("nitrogen fixation", 30, TEXT).move_to(P(0.3, 3.15))
        bact = bchip("bacteria", PURPLE, 28).move_to(P(0.3, 1.85))
        self.at("Nitrogen fixation")
        self.play(FadeOut(block), FadeOut(x), FadeOut(bl), FadeOut(bond), GrowArrow(fix), FadeIn(fl),
                  FadeIn(ammonia), run_time=0.8)
        self.at("certain microbes")
        self.play(FadeIn(bact, shift=DOWN * 0.1), run_time=0.5)

        nitrate = bchip("nitrite, nitrate", GREEN, 36).move_to(P(3.8, 0.1))
        nit = arr(P(3.0, 1.95), P(3.0, 0.65), GREEN, 7)
        nl = T("nitrification", 30, TEXT).move_to(P(5.0, 1.3))
        self.at("Nitrification")
        self.play(GrowArrow(nit), FadeIn(nl), FadeIn(nitrate, shift=UP * 0.1), run_time=0.8)

        as1 = arr(P(3.0, -0.4), P(1.6, -2.0), GREEN, 7)
        al = T("assimilation", 30, TEXT).move_to(P(4.9, -1.3))
        self.at("Assimilation")
        self.play(GrowArrow(as1), FadeIn(al), run_time=0.7)
        ammonium = bchip("ammonium", GREEN, 36).move_to(P(-3.8, 0.1))
        as2 = arr(P(-2.4, -0.45), P(-1.4, -2.0), GREEN, 7)
        self.at("or ammonium")
        self.play(FadeOut(pct), FadeIn(ammonium, shift=UP * 0.1), GrowArrow(as2), run_time=0.7)

        am = arr(P(-5.2, -2.3), P(-5.2, -0.5), ORANGE, 7)
        aml = T("ammonification", 26, TEXT).move_to(P(-3.55, -1.25))
        self.at("Ammonification")
        self.play(GrowArrow(am), FadeIn(aml), run_time=0.7)
        dec = bchip("decomposers", PURPLE, 28).move_to(P(-4.8, -2.85))
        self.at("decomposers turning wastes")
        self.play(FadeIn(dec, shift=UP * 0.1), run_time=0.5)

        dn = arr(P(2.0, 0.35), P(-1.6, 1.85), GREEN, 7)
        dl = T("denitrification", 30, TEXT).move_to(P(-0.2, 0.35))
        dbac = bchip("bacteria", PURPLE, 28).move_to(P(-0.2, -0.45))
        self.at("Denitrification")
        self.play(GrowArrow(dn), FadeIn(dl), run_time=0.7)
        self.at("bacteria turning nitrate")
        self.play(FadeIn(dbac, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    """a ring with a token circling; burning adds old carbon; water carries nitrogen; the cycles link."""

    def construct(self):
        names = [("air", GREY, P(-4.0, 1.9)), ("water", BLUE, P(4.0, 1.9)),
                 ("soil", GREY, P(4.0, -1.9)), ("living things", ORANGE, P(-4.0, -1.9))]
        chips = [bchip(n, c, 44).move_to(p) for n, c, p in names]
        ring = [Line(P(-3.0, 1.9), P(2.9, 1.9), color=GREY, stroke_width=5),
                Line(P(4.0, 1.4), P(4.0, -1.4), color=GREY, stroke_width=5),
                Line(P(3.4, -1.9), P(-1.8, -1.9), color=GREY, stroke_width=5),
                Line(P(-4.0, -1.4), P(-4.0, 1.4), color=GREY, stroke_width=5)]
        self.at("how does matter keep moving")
        self.play(*[FadeIn(c, scale=0.9) for c in chips], run_time=0.8)
        self.at("Atoms are not used up")
        ctok = token("C", YELLOW, 0.33).move_to(P(-3.0, 1.9))
        self.play(FadeIn(ctok), *[Create(a) for a in ring], run_time=0.7)
        self.at("move between air")
        loop = VMobject().set_points_as_corners([P(-3.0, 1.9), P(2.9, 1.9), P(4.0, 1.4), P(4.0, -1.4), P(3.4, -1.9),
                                                 P(-1.8, -1.9), P(-4.0, -1.4), P(-4.0, 1.4), P(-3.0, 1.9)])
        self.play(MoveAlongPath(ctok, loop), run_time=3.6, rate_func=linear)
        form = T("atoms change form", 36, TEXT).move_to(P(0, 0.0))
        self.at("they change form")
        self.play(FadeIn(form), run_time=0.4)

        everything = VGroup(*chips, *ring, ctok, form)
        air2 = bchip("air", GREY, 44).move_to(P(0, 2.0))
        fossil = bchip("coal, oil, natural gas", GREY, 38).move_to(P(0, -0.9))
        up_a = arr(P(0, -0.3), P(0, 1.4), RED, 10)
        blab = T("burning", 36, RED).move_to(P(1.4, 0.55))
        old = T("locked underground\nfor millions of years", 30, GREY, line_spacing=0.8).move_to(P(0, -2.5))
        t = token("C", YELLOW, 0.33).move_to(P(0, -0.3))
        self.at("People can change a cycle")
        self.play(FadeOut(everything), run_time=0.5)
        self.at("Burning coal")
        self.play(FadeIn(air2), FadeIn(fossil), FadeIn(blab), run_time=0.6)
        self.at("adds carbon")
        self.play(GrowArrow(up_a), FadeIn(t), run_time=0.4)
        self.play(t.animate.move_to(P(0, 1.4)), run_time=0.9)
        self.play(FadeOut(t), run_time=0.2)
        self.at("locked underground")
        self.play(FadeIn(old), run_time=0.5)
        burn, add = VGroup(air2, fossil, up_a, blab, old), up_a

        fields = bchip("farm fields", ORANGE, 38).move_to(P(-4.4, 0.0))
        bay = bchip("the Bay", BLUE, 38).move_to(P(4.8, 0.0))
        w = arr(P(-2.5, 0.0), P(3.3, 0.0), BLUE, 10)
        nt = token("N", GREEN, 0.33).move_to(P(-2.5, 0.0))
        self.at("Water carries nitrogen")
        self.play(FadeOut(burn), run_time=0.5)
        self.play(FadeIn(fields), FadeIn(bay), GrowArrow(w), FadeIn(nt), run_time=0.7)
        self.at("toward the Bay")
        self.play(nt.animate.move_to(P(3.3, 0.0)), run_time=1.2)

        self.at("No cycle runs alone")
        carbon = bchip("carbon cycle", YELLOW, 38).move_to(P(-4.2, 1.9))
        water = bchip("water cycle", BLUE, 38).move_to(P(4.2, 1.9))
        nit = bchip("nitrogen cycle", GREEN, 38).move_to(P(0, -1.9))
        l2 = Line(water.get_bottom(), nit.get_right() + UP * 0.0, color=GREY, stroke_width=6)
        l3 = Line(nit.get_left(), carbon.get_bottom(), color=GREY, stroke_width=6)
        self.play(FadeOut(fields), FadeOut(bay), FadeOut(w), FadeOut(nt), run_time=0.4)
        self.play(FadeIn(carbon), FadeIn(water), FadeIn(nit), run_time=0.6)
        self.play(Create(l2), Create(l3), run_time=0.8)
        self.finish()


class S07End(EndCard):
    LINE = "Atoms are not used up. No cycle runs alone."
