"""People change habitats: a new fish in the river  (Biochemistrypedia grade 7 Life Science explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = blue catfish (the invasive fish)
  PURPLE = white catfish (the native fish)
  ORANGE = prey / food supply (small fish, blue crabs)
  YELLOW = people and what people do
  GREEN  = habitat, and populations going up
  RED    = harm: destruction, pollution, populations going down
  TEAL   = the river (water)
  GREY   = outlines, labels, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def fish(color, scale=1.0, flip=False):
    body = Ellipse(width=1.5, height=0.8, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.35)
    tail = Polygon([-0.65, 0, 0], [-1.15, 0.38, 0], [-1.15, -0.38, 0], stroke_color=color, stroke_width=3,
                   fill_color=color, fill_opacity=0.35)
    eye = Dot([0.4, 0.1, 0], radius=0.05, color=TEXT)
    g = VGroup(tail, body, eye).scale(scale)
    if flip:
        g.flip(UP)
    return g


def crab(scale=1.0):
    b = RoundedRectangle(corner_radius=0.15, width=0.9, height=0.55, stroke_color=ORANGE, stroke_width=3,
                         fill_color=ORANGE, fill_opacity=0.35)
    l = Circle(radius=0.17, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.35).move_to([-0.55, 0.38, 0])
    r = Circle(radius=0.17, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.35).move_to([0.55, 0.38, 0])
    return VGroup(l, r, b).scale(scale)


def small_fish(scale=0.5):
    return fish(ORANGE, scale)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def box(w, h, color=GREY, fill=0.08, r=0.2, sw=3):
    return RoundedRectangle(corner_radius=r, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=fill)


def river(x0=-6.0, x1=6.2, y=0.3, h=2.6):
    return box(x1 - x0, h, TEAL, 0.14).move_to([(x0 + x1) / 2, y, 0])


def clear(scene, *keep, t=0.5):
    mobs = [m for m in scene.mobjects if m not in keep]
    if mobs:
        scene.play(*[FadeOut(m) for m in mobs], run_time=t)


def word(text, color=TEXT, size=40):
    return T(text, size, color, weight=BOLD)


class S00Title(TitleCard):
    LESSON = "People change habitats"
    TITLE = "A new fish changes the river"


# ---------------------------------------------------------------------------------------------
class S01Stocked(SpokenScene):
    def construct(self):
        riv = river(-1.5, 6.3, 0.9, 3.4)
        riv_lbl = T("Virginia's Bay rivers", 28, TEAL).next_to(riv, UP, buff=0.15)
        src = box(3.0, 3.4, GREY, 0.08).move_to([-5.2, 0.9, 0])
        src_lbl = T("Mississippi River basin", 24, GREY).next_to(src, UP, buff=0.15)
        bf = fish(BLUE, 0.95).move_to(src.get_center() + LEFT * 0.1)
        bf_lbl = T("blue catfish", 26, BLUE).next_to(src, DOWN, buff=0.2)
        ppl = chip("people", YELLOW, 28).move_to([-2.6, 1.75, 0])
        self.play(FadeIn(riv), FadeIn(riv_lbl), FadeIn(src), FadeIn(src_lbl), FadeIn(bf), FadeIn(bf_lbl), run_time=0.8)
        self.at("people put blue catfish")
        a = arr([-3.55, 0.9, 0], [-1.65, 0.9, 0], YELLOW)
        self.play(FadeIn(ppl, shift=UP * 0.2), GrowArrow(a), run_time=0.6)
        moved = fish(BLUE, 1.0).move_to(bf)
        self.play(moved.animate.move_to([0.3, 0.9, 0]), run_time=1.6)
        when = T("1970s and 1980s", 28, YELLOW).next_to(riv, DOWN, buff=0.25).align_to(riv, RIGHT)
        self.play(FadeIn(when), run_time=0.4)
        self.at("Mississippi River basin")
        self.play(Indicate(VGroup(src, src_lbl), color=GREY, scale_factor=1.05), run_time=0.8)
        self.at("Today they are common")
        pos = [[1.9, 1.9], [3.4, 0.9], [5.0, 1.9], [5.0, 0.0], [2.2, 0.0], [0.3, -0.1]]
        new = [fish(BLUE, 0.9).move_to([x, y, 0]) for x, y in pos]
        self.play(FadeOut(a), FadeOut(ppl), FadeOut(when), LaggedStart(*[FadeIn(n, scale=0.6) for n in new], lag_ratio=0.15), run_time=1.6)
        self.at("what happens to a river")
        clear(self, riv, riv_lbl, moved, *new, t=0.5)
        q = T("What happens to a river\nwhen people bring in\na big new fish?", 40, TEXT, weight=BOLD, line_spacing=0.9)
        q.to_edge(DOWN, buff=0.35)
        riv_up = VGroup(riv, riv_lbl, moved, *new)
        self.play(riv_up.animate.scale(0.9).move_to([0, 1.3, 0]), run_time=0.5)
        q.next_to(riv_up, DOWN, buff=0.4)
        self.play(FadeIn(q, shift=UP * 0.15), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Habitat(SpokenScene):
    def construct(self):
        # A: people are part of ecosystems, depend on food, water, energy
        eco = box(11.0, 5.2, GREEN, 0.06).move_to([0, -0.2, 0])
        eco_lbl = T("ecosystem", 30, GREEN, weight=BOLD).next_to(eco, UP, buff=0.1).align_to(eco, LEFT)
        ppl = chip("people", YELLOW, 40).move_to([3.4, -0.2, 0])
        self.at("People are part of ecosystems")
        self.play(FadeIn(eco), FadeIn(eco_lbl), run_time=0.6)
        self.play(FadeIn(ppl, scale=0.8), run_time=0.5)
        self.at("food water")
        needs = [chip(n, GREEN, 38).move_to([-3.6, y, 0]) for n, y in [("food", 1.5), ("water", -0.2), ("energy", -1.9)]]
        arrs = [arr(n.get_right() + RIGHT * 0.05, ppl.get_left() + LEFT * 0.05, GREEN) for n in needs]
        for n, a in zip(needs, arrs):
            self.play(FadeIn(n), GrowArrow(a), run_time=0.5)
            self.wait(0.15)
        self.at("A habitat is the place")
        clear(self, t=0.5)
        # B: habitat
        hab = box(7.4, 3.6, GREEN, 0.12).move_to([0, 0.5, 0])
        h_lbl = word("habitat", GREEN).to_edge(UP, buff=0.5)
        hf = fish(PURPLE, 1.3).move_to([-0.3, 0.5, 0])
        self.play(FadeIn(h_lbl), FadeIn(hab), run_time=0.5)
        self.play(FadeIn(hf, scale=0.7), run_time=0.4)
        self.at("food water and shelter")
        tags = [chip(n, GREEN, 30) for n in ["food", "water", "shelter"]]
        VGroup(*tags).arrange(RIGHT, buff=0.5).move_to([0, -2.1, 0])
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tags], lag_ratio=0.4), run_time=1.2)
        self.at("A population is all")
        clear(self, t=0.5)
        # C: population
        pop = box(8.4, 3.8, GREY, 0.05).move_to([0, -0.4, 0])
        p_lbl = word("population", PURPLE).to_edge(UP, buff=0.5)
        fishes = [fish(PURPLE, 0.8).move_to([x, y, 0]) for x, y in
                  [(-2.6, 0.5), (0.2, 0.9), (2.5, 0.4), (-1.4, -1.3), (1.6, -1.2)]]
        self.play(FadeIn(p_lbl), FadeIn(pop), run_time=0.5)
        self.at("members of one species")
        self.play(LaggedStart(*[FadeIn(f, scale=0.6) for f in fishes], lag_ratio=0.2), run_time=1.2)
        sp = T("one species", 28, PURPLE).next_to(pop, DOWN, buff=0.2).shift(LEFT * 2.5)
        ar = T("one area", 28, GREY).next_to(pop, DOWN, buff=0.2).shift(RIGHT * 0.2)
        self.play(FadeIn(sp), run_time=0.4)
        self.at("one area")
        self.play(FadeIn(ar), run_time=0.4)
        self.at("Land use is how")
        clear(self, t=0.5)
        # D: land use
        l_lbl = word("land use", YELLOW).to_edge(UP, buff=0.5)
        land = box(3.2, 2.4, GREY, 0.08)
        uses = VGroup(*[chip(n, YELLOW, 44) for n in ["farms", "homes", "roads"]]).arrange(RIGHT, buff=0.8).move_to([0, -0.7, 0])
        ppl2 = chip("people use land", YELLOW, 40).move_to([0, 1.5, 0])
        self.play(FadeIn(l_lbl), FadeIn(ppl2), run_time=0.5)
        self.at("farms homes")
        self.play(LaggedStart(*[GrowFromCenter(u) for u in uses], lag_ratio=0.3), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Destroy(SpokenScene):
    def construct(self):
        # A: taking resources
        lbl = word("taking resources", YELLOW).to_edge(UP, buff=0.5)
        hab = box(4.6, 3.2, GREEN, 0.12).move_to([2.6, -0.6, 0])
        hab_t = T("habitat", 28, GREEN).next_to(hab, UP, buff=0.12)
        res = [chip(n, YELLOW, 32) for n in ["wood", "gravel"]]
        VGroup(*res).arrange(DOWN, buff=0.5).move_to([-3.6, -0.6, 0])
        self.at("Taking resources")
        self.play(FadeIn(lbl), FadeIn(hab), FadeIn(hab_t), run_time=0.6)
        self.at("wood or gravel")
        self.play(*[FadeIn(r, shift=RIGHT * 0.2) for r in res], run_time=0.6)
        ar = arr([-2.1, -0.6, 0], [0.1, -0.6, 0], YELLOW)
        chg = T("changes it", 28, YELLOW).next_to(ar, UP, buff=0.1)
        self.at("changes habitats too")
        self.play(GrowArrow(ar), FadeIn(chg), hab.animate.set_stroke(YELLOW), run_time=0.7)
        self.wait(0.3)
        self.at("Habitat destruction")
        clear(self, t=0.5)
        # B: habitat destruction
        lbl = word("habitat destruction", RED).to_edge(UP, buff=0.5)
        marsh = box(5.2, 3.4, GREEN, 0.18).move_to([-3.4, 0.2, 0])
        marsh_t = T("marsh", 30, GREEN).move_to(marsh)
        an = [small_fish(0.55).move_to(marsh.get_center() + d) for d in [UP * 1.0 + LEFT * 1.4, DOWN * 1.0 + LEFT * 0.4, UP * 1.0 + RIGHT * 1.2]]
        self.play(FadeIn(lbl), FadeIn(marsh), FadeIn(marsh_t), *[FadeIn(a) for a in an], run_time=0.7)
        self.at("Filling in a marsh")
        homes = box(5.2, 3.4, RED, 0.18).move_to(marsh)
        homes_t = T("homes built", 30, RED).move_to(homes)
        self.play(FadeOut(marsh_t), FadeOut(*an) if False else AnimationGroup(*[FadeOut(a) for a in an]),
                  ReplacementTransform(marsh, homes), FadeIn(homes_t), run_time=1.2)
        self.at("Animals there must move or die")
        # population bars (relative, in this sketch)
        base = [1.5, -2.6, 0]
        b1 = Rectangle(width=1.2, height=3.0, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.4).move_to([2.4, -1.6, 0])
        b1.align_to([0, -1.4, 0], DOWN)
        b2 = Rectangle(width=1.2, height=3.0, stroke_color=ORANGE, stroke_width=3, fill_color=ORANGE, fill_opacity=0.4).move_to([4.6, -1.6, 0])
        b2.align_to([0, -1.4, 0], DOWN)
        l1 = T("before", 24, GREY).next_to(b1, DOWN, buff=0.12)
        l2 = T("after", 24, GREY).next_to(b2, DOWN, buff=0.12)
        t1 = T("animals living there", 28, ORANGE).move_to([3.5, 2.4, 0])
        t1.shift(UP * 0.0)
        self.play(FadeIn(b1), FadeIn(b2), FadeIn(l1), FadeIn(l2), FadeIn(t1), run_time=0.6)
        self.at("populations often drop")
        self.play(b2.animate.stretch_to_fit_height(1.0).align_to([0, -1.4, 0], DOWN).set_color(RED), run_time=1.0)
        note = T("in this sketch", 22, GREY).next_to(t1, DOWN, buff=0.12)
        self.play(FadeIn(note), run_time=0.3)
        self.at("Pollution")
        clear(self, t=0.5)
        # C: pollution
        lbl = word("pollution", RED).to_edge(UP, buff=0.5)
        riv = river(-2.8, 6.3, 0.0, 3.0)
        riv_t = T("river", 30, TEAL).next_to(riv, UP, buff=0.12).align_to(riv, LEFT)
        fert = chip("extra fertilizer", RED, 30).move_to([-5.0, 0.0, 0])
        self.play(FadeIn(lbl), FadeIn(riv), FadeIn(riv_t), run_time=0.5)
        self.at("harmful material")
        self.play(FadeIn(fert, shift=RIGHT * 0.2), run_time=0.5)
        self.at("Extra fertilizer in a river")
        self.play(fert.animate.move_to([-0.8, 0.0, 0]), run_time=1.0)
        alg = chip("fast algae growth", GREEN, 30).move_to([4.2, 0.0, 0])
        a = arr([2.9, 0.0, 0], [2.95, 0.0, 0], RED) if False else arr([0.75, 0.0, 0], [2.55, 0.0, 0], RED)
        self.at("fast algae growth")
        can = T("can feed", 24, GREY).next_to(a, UP, buff=0.12)
        self.play(FadeIn(alg, scale=0.8), GrowArrow(a), FadeIn(can), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Invasive(SpokenScene):
    def construct(self):
        # native
        riv = river(-6.0, 6.3, 0.8, 3.0)
        riv_t = T("Virginia's Bay rivers", 26, TEAL).next_to(riv, UP, buff=0.12).align_to(riv, LEFT)
        wf = fish(PURPLE, 1.3).move_to([-3.4, 0.9, 0])
        wl = T("white catfish", 28, PURPLE).next_to(wf, DOWN, buff=0.1)
        nat = word("native species", PURPLE, 36).to_edge(UP, buff=0.35).shift(LEFT * 0.0)
        self.at("A native species lives")
        self.play(FadeIn(riv), FadeIn(riv_t), FadeIn(nat), run_time=0.5)
        self.play(FadeIn(wf, scale=0.7), FadeIn(wl), run_time=0.5)
        nat2 = T("lives here naturally", 30, PURPLE).move_to([0.6, 0.9, 0])
        self.play(FadeIn(nat2), run_time=0.5)
        self.at("native to Virginia's Bay rivers")
        self.play(Indicate(VGroup(wf, wl), color=PURPLE), run_time=0.8)
        self.at("An invasive species is brought")
        inv = word("invasive species", BLUE, 36).move_to(nat)
        self.play(FadeOut(nat), FadeOut(nat2), FadeIn(inv), run_time=0.5)
        bf = fish(BLUE, 1.3).move_to([-5.2, -1.6, 0])
        self.play(FadeIn(bf), run_time=0.3)
        self.play(bf.animate.move_to([3.4, 0.9, 0]), run_time=1.2)
        bl = T("blue catfish", 28, BLUE).next_to(bf, DOWN, buff=0.1)
        self.play(FadeIn(bl), run_time=0.3)
        # three-part test
        parts = [("brought to a new place", "new place"), ("spreads", "spreads"), ("harms native species or people", "harms")]
        rows = []
        for i, (txt, _) in enumerate(parts):
            c = chip(txt, GREY, 28)
            rows.append(c)
        VGroup(*rows).arrange(RIGHT, buff=0.35).move_to([0, -2.1, 0])
        fit(VGroup(*rows), max_w=12.4)
        self.at("Being new is not enough")
        self.play(*[FadeIn(r) for r in rows], run_time=0.6)
        self.play(rows[0][0].animate.set_stroke(YELLOW).set_fill(YELLOW, 0.2), rows[0][1].animate.set_color(YELLOW), run_time=0.4)
        no = T("not enough", 28, RED, weight=BOLD).next_to(rows[0], DOWN, buff=0.15)
        self.play(FadeIn(no), run_time=0.4)
        self.at("It must spread and cause harm")
        self.play(FadeOut(no),
                  *[x for r in rows[1:] for x in (r[0].animate.set_stroke(RED).set_fill(RED, 0.2), r[1].animate.set_color(RED))],
                  run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Compete(SpokenScene):
    def construct(self):
        head = word("competition", ORANGE).to_edge(UP, buff=0.4)
        bf = fish(BLUE, 1.2).move_to([-4.6, 0.2, 0])
        wf = fish(PURPLE, 1.2).move_to([4.6, 0.2, 0], ).flip(RIGHT) if False else fish(PURPLE, 1.2, flip=False).move_to([4.6, 0.2, 0])
        bl = T("blue catfish", 26, BLUE).next_to(bf, DOWN, buff=0.15)
        wl = T("white catfish", 26, PURPLE).next_to(wf, DOWN, buff=0.15)
        # food supply tray
        tray = box(3.6, 3.0, ORANGE, 0.08).move_to([0, 0.2, 0])
        tray_t = T("food supply", 26, ORANGE).next_to(tray, UP, buff=0.12)
        dots = VGroup(*[small_fish(0.38) for _ in range(6)])
        dots.arrange_in_grid(rows=3, cols=2, buff=0.3).move_to(tray)
        self.at("Competition is when")
        self.play(FadeIn(head), run_time=0.4)
        self.play(FadeIn(tray), FadeIn(tray_t), FadeIn(dots), run_time=0.6)
        self.play(FadeIn(bf), FadeIn(bl), FadeIn(wf), FadeIn(wl), run_time=0.6)
        self.at("same resource")
        a1 = arr([-3.4, 0.2, 0], [-1.95, 0.2, 0], BLUE)
        a2 = arr([3.4, 0.2, 0], [1.95, 0.2, 0], PURPLE)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.6)
        self.at("It does not need a fight")
        fight = chip("fight", RED, 30).move_to([0, -2.6, 0])
        cross = Cross(fight, stroke_color=RED, stroke_width=6)
        nof = T("no fight needed", 28, GREY).move_to([0, -2.6, 0])
        self.play(FadeIn(fight), run_time=0.4)
        self.play(Create(cross), run_time=0.4)
        self.wait(0.6)
        self.play(FadeOut(fight), FadeOut(cross), run_time=0.4)
        self.at("Blue catfish eat fish")
        e1 = T("fish, sometimes blue crabs", 26, BLUE).move_to([-4.2, -1.5, 0])
        self.play(Indicate(a1, color=BLUE), FadeIn(e1), run_time=0.8)
        self.at("similar prey")
        e2 = T("similar prey", 26, PURPLE).move_to([4.6, -1.5, 0])
        self.play(Indicate(a2, color=PURPLE), FadeIn(e2), run_time=0.8)
        self.at("may compete for food")
        hedge = T("in this sketch: if blue catfish eat many", 24, ORANGE).move_to([0, -2.05, 0])
        self.play(FadeIn(hedge), run_time=0.4)
        self.wait(0.2)
        self.at("less is left")
        self.play(*[FadeOut(d, scale=0.5) for d in list(dots)[:4]], run_time=1.2)
        left = T("less is left", 28, ORANGE, weight=BOLD).move_to([0, -2.6, 0])
        self.play(FadeIn(left), run_time=0.4)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        head = word("food web", TEXT).to_edge(UP, buff=0.4)
        bf = fish(BLUE, 1.2).move_to([-4.8, 0.4, 0])
        bl = T("blue catfish", 26, BLUE).next_to(bf, DOWN, buff=0.1)
        crabs = VGroup(*[crab(1.0) for _ in range(3)]).arrange(DOWN, buff=0.3).move_to([-0.4, 0.4, 0])
        cl = T("blue crabs", 26, ORANGE).next_to(crabs, DOWN, buff=0.12)
        ce = chip("other crab eaters,\nincluding people", YELLOW, 28).move_to([4.3, 0.4, 0])
        a1 = arr(crabs.get_left() + LEFT * 0.1, bf.get_right() + RIGHT * 0.1, GREY)
        a2 = arr(crabs.get_right() + RIGHT * 0.1, ce.get_left() + LEFT * 0.05, GREY)
        eb = T("eaten by", 24, GREY)
        self.at("A food web links")
        self.play(FadeIn(head), run_time=0.4)
        self.play(FadeIn(bf), FadeIn(bl), FadeIn(crabs), FadeIn(cl), FadeIn(ce), run_time=0.7)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.6)
        e1 = eb.copy().next_to(a1, UP, buff=0.05)
        e2 = eb.copy().next_to(a2, UP, buff=0.05)
        self.play(FadeIn(e1), FadeIn(e2), run_time=0.3)
        self.at("a change in one population")
        self.play(Indicate(bf, color=BLUE), run_time=0.8)
        self.at("blue catfish eat many blue crabs")
        self.play(Indicate(a1, color=BLUE), run_time=0.6)
        self.at("fewer may be left")
        self.play(FadeOut(crabs[1], scale=0.5), FadeOut(crabs[2], scale=0.5), run_time=0.8)
        lessm = T("fewer crabs may be left", 26, ORANGE).next_to(cl, DOWN, buff=0.2)
        self.play(FadeIn(lessm), Indicate(ce, color=YELLOW), run_time=0.6)
        self.at("what happens when people")
        clear(self, t=0.5)
        q = T("What happens to a river when\npeople bring in a big new fish?", 44, TEXT, weight=BOLD, line_spacing=0.9).to_edge(UP, buff=0.7)
        self.play(FadeIn(q), run_time=0.6)
        up = VGroup(Triangle(color=GREEN, fill_opacity=0.5).scale(0.4), T("some populations go up", 44, GREEN)).arrange(RIGHT, buff=0.3)
        dn = VGroup(Triangle(color=RED, fill_opacity=0.5).scale(0.4).rotate(PI), T("others go down", 44, RED)).arrange(RIGHT, buff=0.3)
        VGroup(up, dn).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to([0, -0.5, 0])
        self.at("Some populations go up")
        self.play(FadeIn(up, shift=UP * 0.15), run_time=0.6)
        self.at("others go down")
        self.play(FadeIn(dn, shift=UP * 0.15), run_time=0.6)
        self.at("spreads through the food web")
        sp = T("the change spreads through the food web", 38, TEXT, weight=BOLD).move_to([0, -2.7, 0])
        self.play(FadeIn(sp, shift=UP * 0.15), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "A change in one population spreads through the food web."
