"""Populations rise and fall: why crab numbers rise and fall  (Biochemistrypedia explainer, grade 7 Life Science)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = blue crabs (young and adult), births and crabs moving in
  RED    = losses: deaths, crabs moving out, big crabs that eat young crabs
  GREEN  = grass (a living part of the environment) and the word "biotic"
  TEAL   = nonliving parts of the environment (cold winter, flood) and the word "abiotic"
  YELLOW = actions by people (pollution, hard shorelines, harvest) and the sustainable-harvest plan
  GOLD   = the word "competition"
  TEXT   = survey numbers, questions, the words "population" and "limiting factor"
  GREY   = water, mud, outlines, notes
Dots are schematic crabs ("a sketch, not real counts"). Real numbers on screen: 367 and 852 million crabs
(estimated for the whole Bay, winter dredge survey, winters 1991-1992 and 1992-1993), "about 34 percent fewer"
female crabs than the 2004-2007 average (plan of 2008). Bar heights are computed from those numbers.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

CRAB = BLUE
LOSS = RED
GRASS = GREEN
NONLIVING = TEAL
PEOPLE = YELLOW


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.05, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def dot(color=CRAB, r=0.16):
    return Circle(radius=r, stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.6)


def slots(cx, cy, w, h, n, seed, gap=0.55):
    """n non-overlapping positions inside an ellipse of width w, height h."""
    rng = np.random.default_rng(seed)
    out, tries = [], 0
    while len(out) < n and tries < 20000:
        tries += 1
        p = rng.uniform(-1, 1, 2)
        if p[0] ** 2 + p[1] ** 2 > 0.72:
            continue
        q = np.array([cx + p[0] * w / 2, cy + p[1] * h / 2])
        if all(np.hypot(*(q - o)) > gap for o in out):
            out.append(q)
    return out


class S00Title(TitleCard):
    LESSON = "Populations rise and fall"
    TITLE = "Why Crab Numbers Rise and Fall"


# ---------------------------------------------------------------------------------------------
class S01Crabs(SpokenScene):
    def construct(self):
        ttl = T("Chesapeake Bay, in winter", 36, TEXT, font=TITLE_FONT).move_to([0, 3.0, 0])
        water = Rectangle(width=11.6, height=3.0, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                          fill_opacity=0.08).move_to([0, 0.1, 0])            # y 1.6 .. -1.4
        mud = Rectangle(width=11.6, height=0.8, stroke_color=GREY, stroke_width=2, fill_color=GREY,
                        fill_opacity=0.35).move_to([0, -1.8, 0])             # y -1.4 .. -2.2
        mudl = T("mud", 24, GREY).move_to([-5.1, -2.6, 0])
        boat = chip("survey boat", TEXT, size=28).move_to([-3.6, 2.0, 0])
        dredge = Rectangle(width=0.8, height=0.45, stroke_color=TEXT, stroke_width=3, fill_color=TEXT,
                           fill_opacity=0.25).move_to([-2.5, -1.12, 0])
        tow = always_redraw(lambda: Line(boat.get_bottom() + DOWN * 0.02, dredge.get_top() + LEFT * 0.2,
                                         color=GREY, stroke_width=4))
        dlab = T("dredge", 24, TEXT).move_to([-1.5, -0.85, 0])
        dlab.add_updater(lambda m: m.move_to(dredge.get_center() + [1.05, 0.05, 0]))
        crabs = VGroup(*[dot(CRAB, 0.17).move_to([x, -1.8, 0]) for x in (-4.3, -3.0, -1.4, 0.0, 1.3, 2.7, 4.1)])
        cl = T("blue crabs buried in the mud", 26, CRAB).move_to([1.2, -2.7, 0])

        self.at("Every winter")
        self.play(FadeIn(ttl, shift=DOWN * 0.1), FadeIn(water), FadeIn(mud), FadeIn(mudl),
                  FadeIn(boat, shift=DOWN * 0.1), run_time=1.0)
        self.at("tow dredges")
        self.add(tow)
        self.play(FadeIn(dredge, shift=DOWN * 0.2), FadeIn(dlab), run_time=0.8)
        self.play(boat.animate.shift(RIGHT * 2.4), dredge.animate.shift(RIGHT * 2.4), run_time=2.8, rate_func=linear)
        self.at("They catch blue crabs")
        self.play(FadeIn(crabs, lag_ratio=0.12), FadeIn(cl), run_time=1.2)
        est = chip("estimate for the whole Bay", YELLOW, size=26).move_to([3.9, 2.05, 0])
        a_est = arr(boat.get_right() + RIGHT * 0.1, est.get_left() + LEFT * 0.05, YELLOW, w=5)
        self.at("estimate how many")
        self.play(GrowArrow(a_est), FadeIn(est, shift=LEFT * 0.2), run_time=1.0)

        # bars, computed from 367 and 852 (million), baseline y = -2.2, 852 -> 4.0 tall
        H = 4.0
        h1, h2 = H * 367 / 852, H
        base = -2.2
        b1 = Rectangle(width=1.8, height=h1, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.35)
        b1.move_to([-2.2, base + h1 / 2, 0])
        b2 = Rectangle(width=1.8, height=h2, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.35)
        b2.move_to([2.2, base + h2 / 2, 0])
        axis = Line([-3.6, base, 0], [3.6, base, 0], color=GREY, stroke_width=3)
        t1 = VGroup(M("367", 40, TEXT), T("million", 24, GREY)).arrange(RIGHT, buff=0.15, aligned_edge=DOWN)
        t1.next_to(b1, UP, buff=0.15)
        t2 = VGroup(M("852", 40, TEXT), T("million", 24, GREY)).arrange(RIGHT, buff=0.15, aligned_edge=DOWN)
        t2.next_to(b2, UP, buff=0.15)
        w1 = T("winter 1991–1992", 24, GREY).next_to(b1, DOWN, buff=0.15)
        w2 = T("winter 1992–1993", 24, GREY).next_to(b2, DOWN, buff=0.15)
        ctitle = T("estimated blue crabs in the whole Bay", 30, TEXT).move_to([0, 3.0, 0])
        dash = DashedLine([-3.1, base + 2 * h1, 0], [3.1, base + 2 * h1, 0], color=YELLOW, stroke_width=4, dash_length=0.18)
        dl = M("2 × 367 = 734", 26, YELLOW).move_to([-2.2, base + 2 * h1 + 0.4, 0])
        notbig = T("The Bay did not get bigger.", 32, TEXT).move_to([0, -3.3, 0])

        self.at("From one winter")
        self.play(*[FadeOut(m) for m in (ttl, water, mud, mudl, boat, dredge, crabs, cl, est, a_est, dlab, tow)], run_time=0.3)
        self.remove(tow, dlab)
        self.play(FadeIn(ctitle), Create(axis), FadeIn(b1, shift=UP * 0.2), FadeIn(t1), FadeIn(w1), run_time=0.45)
        self.at("to the next")
        self.play(FadeIn(b2, shift=UP * 0.2), FadeIn(t2), FadeIn(w2), run_time=0.7)
        self.at("more than doubled")
        self.play(Create(dash), FadeIn(dl), Indicate(b2, color=YELLOW, scale_factor=1.03), run_time=1.0)
        self.at("did not get bigger")
        self.play(FadeIn(notbig, shift=UP * 0.1), run_time=0.6)
        q = T("Why are there lots of crabs some years,\nand far fewer in others?", 44, TEXT, font=TITLE_FONT, line_spacing=0.8)
        fit(q, max_w=11.6, max_h=2.2)
        q.move_to([0, 0, 0])
        self.at("So why are there")
        self.play(*[FadeOut(m) for m in (ctitle, axis, b1, b2, t1, t2, w1, w2, dash, dl, notbig)], run_time=0.6)
        self.play(Write(q), run_time=2.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Population(SpokenScene):
    def construct(self):
        cx, cy = 0.0, -0.2
        bay = Ellipse(width=5.2, height=4.2, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.10).move_to([cx, cy, 0])
        baylab = T("the Bay", 26, GREY).move_to([cx, cy - 2.4, 0])
        pos = slots(cx, cy, 5.2, 4.2, 14, seed=11, gap=0.62)
        dots = [dot(CRAB, 0.17).move_to([*p, 0]) for p in pos]
        n = {"v": 0}

        def setn(k):
            anims = []
            if k > n["v"]:
                anims += [FadeIn(d, scale=0.5) for d in dots[n["v"]:k]]
            elif k < n["v"]:
                anims += [FadeOut(d) for d in dots[k:n["v"]]]
            n["v"] = k
            return anims

        pop = T("population", 40, TEXT, weight=BOLD).move_to([0, 3.0, 0])
        defn = T("all the members of one species in one place", 28, GREY).move_to([0, 2.45, 0])
        births = chip("births", CRAB, size=30).move_to([-5.0, 1.0, 0])
        movin = chip("move in", CRAB, size=30).move_to([-5.0, -1.4, 0])
        deaths = chip("deaths", LOSS, size=30).move_to([5.0, 1.0, 0])
        movout = chip("move out", LOSS, size=30).move_to([5.0, -1.4, 0])
        ab = arr(births.get_right() + RIGHT * 0.1, [-2.35, 0.9, 0], CRAB, w=6)
        ai = arr(movin.get_right() + RIGHT * 0.1, [-2.35, -1.3, 0], CRAB, w=6)
        ad = arr([2.35, 0.9, 0], deaths.get_left() + LEFT * 0.1, LOSS, w=6)
        ao = arr([2.35, -1.3, 0], movout.get_left() + LEFT * 0.1, LOSS, w=6)
        note = T("dots are a sketch, not real counts", 22, GREY).move_to([0, -3.3, 0])

        self.at("A population is")
        self.play(FadeIn(pop, shift=DOWN * 0.1), FadeIn(defn), FadeIn(bay), run_time=1.0)
        self.at("The blue crabs in the Bay")
        self.play(FadeIn(baylab), *setn(8), FadeIn(note), run_time=1.2)
        self.play(Indicate(VGroup(*dots[:8]), color=CRAB, scale_factor=1.05), run_time=0.8)
        self.at("Births add")
        self.play(FadeIn(births, scale=0.9), GrowArrow(ab), *setn(10), run_time=1.0)
        self.at("So do crabs moving in")
        self.play(FadeIn(movin, scale=0.9), GrowArrow(ai), *setn(12), run_time=1.0)
        self.at("Deaths take")
        self.play(FadeIn(deaths, scale=0.9), GrowArrow(ad), *setn(10), run_time=1.0)
        self.at("So do crabs moving out")
        self.play(FadeIn(movout, scale=0.9), GrowArrow(ao), *setn(8), run_time=1.0)
        grows = VGroup(T("grows", 40, CRAB, weight=BOLD)).move_to([3.7, -2.9, 0])
        shrinks = VGroup(T("shrinks", 40, LOSS, weight=BOLD)).move_to([-3.7, -2.9, 0])
        self.at("more are added than lost")
        self.play(*setn(12), FadeIn(grows, shift=UP * 0.15), Indicate(VGroup(ab, ai), color=CRAB), run_time=1.2)
        self.at("When more are lost")
        self.play(*setn(5), FadeOut(grows), run_time=1.2)
        self.at("it shrinks")
        self.play(FadeIn(shrinks, shift=DOWN * 0.15), Indicate(VGroup(ad, ao), color=LOSS), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Factors(SpokenScene):
    def construct(self):
        head = chip("limiting factor", TEXT, size=40).move_to([0, 3.0, 0])
        hdef = T("anything that keeps a population from growing larger", 28, GREY).move_to([0, 2.15, 0])
        bio = chip("biotic: living", GRASS, size=40).move_to([-3.2, 1.0, 0])
        abio = chip("abiotic: nonliving", NONLIVING, size=40).move_to([3.2, 1.0, 0])
        big = dot(LOSS, 0.6).move_to([-4.7, -0.6, 0])
        biglab = T("big crab", 26, LOSS).next_to(big, DOWN, buff=0.15)
        young = VGroup(*[dot(CRAB, 0.2).move_to([-2.5 + 0.7 * i, -0.6 + (0.3 if i % 2 else -0.3), 0]) for i in range(4)])
        ylab = T("young crabs", 26, CRAB).move_to([-1.5, -1.5, 0])
        eats = arr(big.get_right() + RIGHT * 0.05, [-2.95, -0.6, 0], LOSS, w=5)
        eatlab = T("big crabs eat many\nyoung crabs", 30, TEXT, line_spacing=0.8).move_to([-3.2, -2.55, 0])
        cold = chip("very cold winter", NONLIVING, size=36).move_to([3.2, -0.2, 0])
        row = VGroup(*[dot(CRAB, 0.2).move_to([1.2 + 0.8 * i, -1.4, 0]) for i in range(6)])
        die = T("more crabs die\nbefore spring", 30, TEXT, line_spacing=0.8).move_to([3.2, -2.55, 0])
        sk = T("a sketch, not real counts", 24, GREY).move_to([3.2, -3.5, 0])

        self.at("A limiting factor")
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.6)
        self.play(FadeIn(hdef), run_time=0.8)
        self.at("A biotic factor")
        self.play(FadeIn(bio, scale=0.9), run_time=0.7)
        self.at("Big crabs eat")
        self.play(FadeIn(big, scale=0.8), FadeIn(biglab), FadeIn(young, lag_ratio=0.1), FadeIn(ylab), run_time=1.0)
        self.play(GrowArrow(eats), FadeIn(eatlab, shift=UP * 0.1), run_time=0.8)
        self.at("An abiotic factor")
        self.play(FadeIn(abio, scale=0.9), run_time=0.7)
        self.at("very cold winter")
        self.play(FadeIn(cold, scale=0.9), FadeIn(row, lag_ratio=0.1), FadeIn(sk), run_time=1.0)
        self.at("more crabs die")
        self.play(FadeOut(row[3:]), FadeIn(die, shift=UP * 0.1), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Hiding(SpokenScene):
    def construct(self):
        top = T("shallow water and grass", 36, GRASS).move_to([0, 3.0, 0])
        px = [-4.0, -0.7, 2.6]
        patches = [RoundedRectangle(corner_radius=0.2, width=3.0, height=2.0, stroke_color=GRASS, stroke_width=3,
                                    fill_color=GRASS, fill_opacity=0.25).move_to([x, 0.8, 0]) for x in px]
        crabs = [[dot(CRAB, 0.2).move_to([x - 0.5 + 1.0 * j, 0.8, 0]) for j in range(2)] for x in px]
        big = dot(LOSS, 0.6).move_to([5.4, 0.8, 0])
        biglab = T("big crab", 26, LOSS).next_to(big, DOWN, buff=0.15)
        ylab = T("young crabs", 26, CRAB).move_to([px[0], -0.5, 0])
        glab = T("grass", 26, GRASS).move_to([px[1], -0.5, 0])
        grid = [[-1.5, 1.15], [-0.7, 1.15], [0.1, 1.15], [-1.5, 0.45], [-0.7, 0.45], [0.1, 0.45]]
        comp = chip("competition", GOLD, size=40).move_to([0, -1.5, 0])
        cdef = T("more young crabs need the same hiding place", 30, TEXT).move_to([0, -2.25, 0])
        c1 = chip("a limiting factor changes", TEXT, size=26)
        c2 = chip("the population can change", TEXT, size=26)
        mid = arr(LEFT, RIGHT, GREY, w=5)
        row = VGroup(c1, mid.scale(0.7), c2).arrange(RIGHT, buff=0.25).move_to([0, -3.05, 0])
        fit(row, max_w=12.2, max_h=0.9)

        self.at("Young crabs can hide")
        self.play(FadeIn(top, shift=DOWN * 0.1), *[FadeIn(p) for p in patches], run_time=0.6)
        self.play(*[FadeIn(d, scale=0.6) for g in crabs for d in g], FadeIn(ylab), FadeIn(glab), run_time=0.6)
        self.at("from big crabs")
        self.play(FadeIn(big, scale=0.8), FadeIn(biglab), run_time=0.8)
        self.at("With less grass")
        self.play(FadeOut(patches[0]), FadeOut(patches[2]), FadeOut(ylab), run_time=0.9)
        moves = []
        for d, p in zip([crabs[0][0], crabs[0][1], crabs[1][0], crabs[1][1], crabs[2][0], crabs[2][1]], grid):
            moves.append(d.animate.move_to([p[0], p[1], 0]))
        self.at("more young crabs need")
        self.play(*moves, run_time=1.3)
        self.play(Indicate(patches[1], color=GRASS, scale_factor=1.05), run_time=0.8)
        self.at("That need is called")
        self.play(FadeIn(comp, scale=0.9), run_time=0.8)
        self.play(FadeIn(cdef, shift=UP * 0.1), run_time=0.8)
        self.at("When a limiting factor changes")
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.7)
        self.at("the population can change")
        self.play(FadeIn(row[1]), FadeIn(c2, shift=LEFT * 0.1), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Causes(SpokenScene):
    def construct(self):
        nh = T("natural", 42, NONLIVING, weight=BOLD).move_to([-3.3, 2.8, 0])
        ph = T("caused by people", 42, PEOPLE, weight=BOLD).move_to([3.3, 2.8, 0])
        cold = chip("cold winters", NONLIVING, size=38).move_to([-3.3, 1.5, 0])
        flood = chip("floods", NONLIVING, size=38).move_to([-3.3, 0.4, 0])
        poll = chip("pollution", PEOPLE, size=38).move_to([3.3, 1.7, 0])
        hard = chip("hard shorelines", PEOPLE, size=38).move_to([3.3, 0.6, 0])
        hcap = T("can shrink the shallow water\nwhere young crabs hide", 26, GREY, line_spacing=0.8).move_to([3.3, -0.4, 0])
        over = chip("overharvesting", PEOPLE, size=38).move_to([3.3, -1.4, 0])
        odef = T("people catch a species\nfaster than it can replace itself", 36, TEXT, line_spacing=0.8).move_to([0, -2.85, 0])
        divider = Line([0, 3.3, 0], [0, -1.8, 0], color=GREY, stroke_width=2).set_opacity(0.5)

        self.at("Some causes are natural")
        self.play(FadeIn(nh, shift=DOWN * 0.1), FadeIn(divider), run_time=0.7)
        self.at("cold winters and floods")
        self.play(FadeIn(cold, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(flood, shift=UP * 0.1), run_time=0.6)
        self.at("People cause changes")
        self.play(FadeIn(ph, shift=DOWN * 0.1), run_time=0.7)
        self.at("One is pollution")
        self.play(FadeIn(poll, shift=UP * 0.1), run_time=0.7)
        self.at("Another is")
        self.play(FadeIn(hard, shift=UP * 0.1), run_time=0.7)
        self.at("shrink the shallow water")
        self.play(FadeIn(hcap, shift=UP * 0.1), run_time=0.8)
        self.at("A third is")
        self.play(FadeIn(over, shift=UP * 0.1), run_time=0.7)
        self.at("That means people catch")
        self.play(FadeIn(odef, shift=UP * 0.1), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    def construct(self):
        # phase 1: the 2008 plan, bar heights computed from "about 34 percent fewer" (1.0 -> 0.66)
        ttl = T("2008: Virginia and Maryland plan", 34, TEXT).move_to([0, 3.1, 0])
        base = -0.9
        H = 2.7
        hp = H * (1 - 0.34)
        bar1 = Rectangle(width=2.0, height=H, stroke_color=PEOPLE, stroke_width=3, fill_color=PEOPLE, fill_opacity=0.18).move_to([-4.4, base + H / 2, 0])
        bar2 = Rectangle(width=2.0, height=hp, stroke_color=PEOPLE, stroke_width=3, fill_color=PEOPLE, fill_opacity=0.5).move_to([-1.8, base + hp / 2, 0])
        axis = Line([-5.8, base, 0], [-0.4, base, 0], color=GREY, stroke_width=3)
        ylab = T("female crabs caught (relative)", 28, TEXT).move_to([-3.1, base + H + 0.45, 0])
        l1 = T("2004 to 2007\naverage", 24, GREY, line_spacing=0.8).next_to(bar1, DOWN, buff=0.15)
        l2 = T("2008 plan:\nabout 34% fewer", 24, PEOPLE, line_spacing=0.8).next_to(bar2, DOWN, buff=0.15)
        fem = chip("females carry the eggs", CRAB, size=30).move_to([3.4, 1.9, 0])
        young = VGroup(*[dot(CRAB, 0.16).move_to([1.9 + 0.65 * i, -0.2, 0]) for i in range(5)])
        mean = T("can mean", 28, GREY).move_to([4.5, 0.85, 0])
        a_down = arr([3.4, 1.4, 0], [3.4, 0.35, 0], GREY, w=5)
        ylab2 = T("more young crabs later", 30, CRAB).move_to([3.4, -0.9, 0])
        sus = chip("sustainable harvest", PEOPLE, size=40).move_to([0, -2.45, 0])
        sdef = T("take only as many as the population can replace", 30, TEXT).move_to([0, -3.15, 0])

        self.at("made a plan")
        self.play(FadeIn(ttl, shift=DOWN * 0.1), Create(axis), FadeIn(bar1, shift=UP * 0.2), FadeIn(l1), FadeIn(ylab), run_time=1.2)
        self.at("fewer female crabs")
        self.play(FadeIn(bar2, shift=UP * 0.2), FadeIn(l2), run_time=1.0)
        self.at("Females carry the eggs")
        self.play(FadeIn(fem, shift=DOWN * 0.1), run_time=0.8)
        self.at("leaving more of them")
        self.play(Indicate(bar2, color=PEOPLE, scale_factor=1.04), run_time=0.8)
        self.at("can mean more young crabs")
        self.play(GrowArrow(a_down), FadeIn(mean), FadeIn(young, lag_ratio=0.15), FadeIn(ylab2), run_time=1.4)
        self.at("Taking only as many")
        self.play(FadeIn(sus, scale=0.9), run_time=0.8)
        self.play(FadeIn(sdef, shift=UP * 0.1), run_time=0.8)

        # phase 2: a limit is not a promise
        lim = T("a limit is not a promise", 46, TEXT, font=TITLE_FONT).move_to([0, 1.3, 0])
        tl = Arrow([-4.5, -0.6, 0], [4.5, -0.6, 0], color=GREY, stroke_width=6, buff=0, tip_length=0.3)
        tlab = T("rebuilding can take years", 34, TEXT).move_to([0, -1.5, 0])
        self.at("not a promise")
        self.play(*[FadeOut(m) for m in (ttl, axis, bar1, bar2, l1, l2, ylab, fem, young, mean, a_down, ylab2, sus, sdef)], run_time=0.6)
        self.play(Write(lim), run_time=1.0)
        self.at("rebuilding can take")
        self.play(GrowArrow(tl), FadeIn(tlab, shift=UP * 0.1), run_time=1.4)

        # phase 3: the answer
        q = T("Why lots of crabs some years, and far fewer in others?", 32, GREY).move_to([0, 3.0, 0])
        crabsn = chip("number of crabs", CRAB, size=46).move_to([0, 0.0, 0])
        f1 = chip("cold winters", NONLIVING, size=34).move_to([-4.0, 1.7, 0])
        f2 = chip("hiding places", GRASS, size=34).move_to([4.0, 1.7, 0])
        f3 = chip("big crabs", LOSS, size=34).move_to([-4.0, -1.7, 0])
        f4 = chip("harvest", PEOPLE, size=34).move_to([4.0, -1.7, 0])
        arrows = [arr(f1.get_bottom() + DOWN * 0.05, crabsn.get_left() + UP * 0.15 + LEFT * 0.1, NONLIVING),
                  arr(f2.get_bottom() + DOWN * 0.05, crabsn.get_right() + UP * 0.15 + RIGHT * 0.1, GRASS),
                  arr(f3.get_top() + UP * 0.05, crabsn.get_left() + DOWN * 0.15 + LEFT * 0.1, LOSS),
                  arr(f4.get_top() + UP * 0.05, crabsn.get_right() + DOWN * 0.15 + RIGHT * 0.1, PEOPLE)]
        ans = T("The things that limit crabs keep changing.", 40, TEXT, font=TITLE_FONT).move_to([0, -3.0, 0])
        fit(ans, max_w=12.0)
        self.at("So why does")
        self.play(FadeOut(lim), FadeOut(tl), FadeOut(tlab), run_time=0.6)
        self.play(FadeIn(q, shift=DOWN * 0.1), FadeIn(crabsn, scale=0.9), run_time=0.8)
        self.at("The things that")
        self.play(FadeIn(ans, shift=UP * 0.1),
                  *[FadeIn(f, scale=0.9) for f in (f1, f2, f3, f4)], *[GrowArrow(a) for a in arrows], run_time=1.2)
        self.at("keep changing")
        self.play(*[Indicate(f, color=c, scale_factor=1.12) for f, c in ((f1, NONLIVING), (f2, GRASS), (f3, LOSS), (f4, PEOPLE))], run_time=1.4)
        self.finish()


class S07End(EndCard):
    LINE = "The things that limit crabs keep changing."
