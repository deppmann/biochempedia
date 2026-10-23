"""Adaptations for survival: a white hare on bare ground  (Biochemistrypedia grade 7 Life Science explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = adaptation / the inherited trait (word chip, the coat trait passed to young)
  TEAL   = physical adaptation
  ORANGE = behavioral adaptation
  GREEN  = blends in / helps / timing that fits the snow
  RED    = stands out / costs / cannot (crossed out)
  PURPLE = predator, and variation
  YELLOW = the question, trade-off, and population (the key terms the film is about)
  GREY   = outlines, ground lines, de-emphasised labels
  Coat colors: white coat #F4F6FA, brown coat #8A6240 (the objects themselves, not concepts).
  Snow band #D5E1EE, bare brown ground #5B4331.
All hares are one labelled block silhouette (body, head, ears, feet). No molecules, no data plots:
the film uses no numbers.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"
WHITE_C = "#F4F6FA"
BROWN_C = "#8A6240"
SNOW_C = "#D5E1EE"
GROUND_C = "#5B4331"
EDGE = "#9AA3B2"
INK = "#1B2433"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def hare(coat=WHITE_C, s=1.0, edge=EDGE):
    """A snowshoe hare as one outlined silhouette made of block shapes. Feet at y=0 (before scale)."""
    def rr(w, h, x, y, r):
        return RoundedRectangle(corner_radius=r, width=w, height=h).move_to([x, y, 0])
    parts = [
        rr(2.5, 1.25, 0.0, 0.95, 0.6),      # body
        rr(0.95, 0.8, 1.45, 1.55, 0.35),    # head
        rr(0.26, 0.95, 1.3, 2.3, 0.13).rotate(-0.12),   # ear
        rr(0.26, 0.95, 1.62, 2.25, 0.13).rotate(0.1),   # ear
        rr(1.1, 0.3, -0.75, 0.15, 0.15),    # big back foot
        rr(0.32, 0.45, 0.85, 0.22, 0.12),   # front leg
    ]
    body = Union(*parts, stroke_color=edge, stroke_width=3, fill_color=coat, fill_opacity=1)
    eye = Dot([1.66, 1.65, 0], radius=0.06, color=BG)
    g = VGroup(body, eye)
    g.body = body
    g.scale(s)
    return g


def stand(h, x, feet_y):
    h.move_to([x, feet_y + h.height / 2, 0])
    return h


def bchip(text, color=BLUE, size=26, **kw):
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def btext(text, size=26, color=TEXT):
    t = T(text, size, color)
    back = Rectangle(width=t.width + 0.24, height=t.height + 0.14, stroke_width=0, fill_color=BG,
                     fill_opacity=0.92).move_to(t)
    return VGroup(back, t)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def band(x, y_top, y_bot, w, color):
    return Rectangle(width=w, height=y_top - y_bot, stroke_width=0, fill_color=color,
                     fill_opacity=1).move_to([x, (y_top + y_bot) / 2, 0])


def cross_out(mob, color=RED):
    a = Line(mob.get_corner(UL), mob.get_corner(DR), color=color, stroke_width=7)
    b = Line(mob.get_corner(DL), mob.get_corner(UR), color=color, stroke_width=7)
    return VGroup(a, b)


def recoat(h, color):
    return h.body.animate.set_fill(color, 1)


class S00Title(TitleCard):
    LESSON = "Adaptations for survival"
    TITLE = "A white hare on bare ground"


# ---------------------------------------------------------------------------------------------
class S01Hare(SpokenScene):
    """brown hare on brown ground -> turns white as snow arrives -> hard to see -> snow melts, still white -> ?"""

    def construct(self):
        ground = band(0, -1.9, -3.5, 12.6, GROUND_C)
        h = stand(hare(BROWN_C, 1.3), 0, -1.9)
        name = T("snowshoe hare", 30, TEXT).move_to([0, 2.45, 0])
        place = T("brown ground", 28, TEXT).move_to([0, -2.7, 0])
        self.at("snowshoe")
        self.play(FadeIn(ground), FadeIn(h, shift=UP * 0.2), FadeIn(name), FadeIn(place), run_time=0.8)

        self.at("turns white")
        snow = T("snow", 28, INK).move_to([0, -2.7, 0])
        self.play(ground.animate.set_fill(SNOW_C), recoat(h, WHITE_C),
                  ReplacementTransform(place, snow), run_time=2.2)

        self.at("hard to see")
        hard = bchip("hard to see", GREEN, 30).move_to([4.6, 0.0, 0])
        self.play(FadeIn(hard, shift=LEFT * 0.2), run_time=0.5)

        self.at("snow melts early")
        place2 = T("snow melts early", 28, TEXT).move_to([0, -2.7, 0])
        self.play(ground.animate.set_fill(GROUND_C), FadeOut(hard), FadeOut(snow),
                  FadeIn(place2), run_time=1.3)

        self.at("still white")
        still = bchip("still white", YELLOW, 30).move_to([-4.6, 0.0, 0])
        self.play(FadeIn(still, shift=RIGHT * 0.2), Indicate(h, color=WHITE_C, scale_factor=1.04), run_time=0.9)

        self.at("What happens")
        q = T("?", 150, YELLOW, weight=BOLD).move_to([4.6, 0.0, 0])
        qt = T("What happens to this hare?", 36, YELLOW).move_to([0, 3.2, 0])
        self.play(FadeIn(q, scale=0.6), Write(qt), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Adaptation(SpokenScene):
    """adaptation = inherited trait that helps survive and reproduce; parent hare passes the trait to young."""

    def construct(self):
        word = bchip("adaptation", BLUE, 48).move_to([0, 3.05, 0])
        self.at("An adaptation")
        self.play(FadeIn(word, scale=0.85), run_time=0.6)

        trait = bchip("inherited trait", BLUE, 36).move_to([-3.8, 1.0, 0])
        self.at("inherited trait")
        self.play(FadeIn(trait, shift=UP * 0.2), run_time=0.5)

        surv = bchip("survive", GREEN, 36).move_to([1.8, 1.75, 0])
        a1 = arr(trait.get_right() + [0.02, 0.2, 0], surv.get_left(), BLUE)
        self.at("survive")
        self.play(GrowArrow(a1), FadeIn(surv, shift=RIGHT * 0.2), run_time=0.6)

        rep = bchip("reproduce", GREEN, 36).move_to([1.6, 0.25, 0])
        a2 = arr(trait.get_right() + [0.02, -0.2, 0], rep.get_left(), BLUE)
        self.at("reproduce")
        self.play(GrowArrow(a2), FadeIn(rep, shift=RIGHT * 0.2), run_time=0.6)
        young_t = T("= have young", 34, GREEN).next_to(rep, RIGHT, buff=0.3)
        self.at("have young")
        self.play(FadeIn(young_t, shift=LEFT * 0.2), run_time=0.5)

        parent = stand(hare(WHITE_C, 0.9, edge=BLUE), -4.0, -3.0)
        par_l = T("parent", 28, GREY).move_to([-4.0, -3.4, 0])
        self.at("Inherited means")
        self.play(FadeIn(parent, shift=UP * 0.2), FadeIn(par_l), run_time=0.6)
        pas = arr([-2.4, -1.7, 0], [-0.3, -1.7, 0], BLUE)
        pas_l = T("passes to", 28, BLUE).next_to(pas, UP, buff=0.12)
        y1 = stand(hare(WHITE_C, 0.5, edge=BLUE), 0.9, -3.0)
        y2 = stand(hare(WHITE_C, 0.5, edge=BLUE), 2.7, -3.0)
        y_l = T("their young", 28, GREY).move_to([1.8, -3.4, 0])
        self.at("passes from parents")
        self.play(GrowArrow(pas), FadeIn(pas_l), run_time=0.5)
        self.at("to their young")
        self.play(FadeIn(y1, shift=LEFT * 0.2), FadeIn(y2, shift=LEFT * 0.2), FadeIn(y_l), run_time=0.7)

        self.at("white coat is one")
        tag = bchip("white coat", BLUE, 34).move_to([4.9, -1.7, 0])
        self.play(FadeIn(tag, shift=LEFT * 0.2), Indicate(parent, color=BLUE, scale_factor=1.05),
                  Indicate(y1, color=BLUE, scale_factor=1.1), Indicate(y2, color=BLUE, scale_factor=1.1),
                  run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Types(SpokenScene):
    """left: physical (covering, color, structure; heron legs). right: behavioral (migration; monarchs south)."""

    def construct(self):
        div = Line([0, 3.3, 0], [0, -3.4, 0], color=GREY, stroke_width=2, stroke_opacity=0.5)
        self.add(div)
        ph = bchip("physical adaptation", TEAL, 32).move_to([-3.3, 3.0, 0])
        self.at("A physical adaptation")
        self.play(FadeIn(ph, shift=DOWN * 0.15), run_time=0.5)
        feat = T("a feature of the body", 28, TEXT).move_to([-3.3, 2.15, 0])
        self.at("feature of the body")
        self.play(FadeIn(feat), run_time=0.4)
        c1 = bchip("body covering", TEAL, 24)
        c2 = bchip("color", TEAL, 24)
        c3 = bchip("structure", TEAL, 24)
        row = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.12).move_to([-3.35, 1.3, 0])
        self.at("body covering")
        self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.35)
        self.at("a color")
        self.play(FadeIn(c2, shift=UP * 0.15), run_time=0.35)
        self.at("or a structure")
        self.play(FadeIn(c3, shift=UP * 0.15), run_time=0.35)

        water = band(-3.3, -2.45, -3.4, 5.4, GREY)
        water.set_fill(GREY, 0.28)
        hb = RoundedRectangle(corner_radius=0.25, width=1.5, height=0.7, stroke_color=TEAL, stroke_width=4,
                              fill_color=TEAL, fill_opacity=0.28).move_to([-3.3, -0.2, 0])
        neck = Line([-2.65, 0.1, 0], [-2.65, 0.58, 0], color=TEAL, stroke_width=6)
        hd = RoundedRectangle(corner_radius=0.1, width=0.62, height=0.28, stroke_color=TEAL, stroke_width=4,
                              fill_color=TEAL, fill_opacity=0.28).move_to([-2.4, 0.64, 0])
        heron_top = VGroup(hb, neck, hd)
        legs = VGroup(Line([-3.65, -0.55, 0], [-3.65, -2.95, 0], color=TEAL, stroke_width=7),
                      Line([-2.95, -0.55, 0], [-2.95, -2.95, 0], color=TEAL, stroke_width=7))
        hl = T("heron: long legs", 26, TEAL).move_to([-1.0, -1.4, 0])
        self.at("long legs")
        self.play(FadeIn(water), FadeIn(heron_top), run_time=0.5)
        self.play(*[Create(l) for l in legs], FadeIn(hl), run_time=0.9)

        be = bchip("behavioral adaptation", ORANGE, 32).move_to([3.3, 3.0, 0])
        self.at("A behavioral adaptation")
        self.play(FadeIn(be, shift=DOWN * 0.15), run_time=0.5)
        act = T("an action", 28, TEXT).move_to([3.3, 2.15, 0])
        self.at("is an action")
        self.play(FadeIn(act), run_time=0.4)
        mig = bchip("migration", ORANGE, 30).move_to([3.3, 1.2, 0])
        self.at("Migration")
        self.play(FadeIn(mig, shift=UP * 0.15), run_time=0.5)
        jr = VGroup(T("a regular journey between", 26, TEXT), T("places used in different seasons", 26, TEXT)
                    ).arrange(DOWN, buff=0.12).move_to([3.3, 0.2, 0])
        self.at("regular journey")
        self.play(FadeIn(jr), run_time=0.6)
        path = arr([3.3, -0.55, 0], [3.3, -2.35, 0], ORANGE, w=7)
        south = T("south", 28, ORANGE).move_to([4.5, -1.45, 0])
        mon = bchip("monarchs fly south in fall", ORANGE, 26).move_to([3.3, -3.0, 0])
        self.at("Monarch butterflies")
        self.play(GrowArrow(path), FadeIn(south), run_time=0.8)
        self.play(FadeIn(mon, shift=UP * 0.15), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Camouflage(SpokenScene):
    """white hare on snow (blends in) vs on bare ground (stands out); predator looks at each; helps / costs."""

    def construct(self):
        XL, XR = -3.2, 3.2
        snow = band(XL, -2.1, -3.4, 5.8, SNOW_C)
        gr = band(XR, -2.1, -3.4, 5.8, GROUND_C)
        div = Line([0, 2.0, 0], [0, -3.4, 0], color=GREY, stroke_width=2, stroke_opacity=0.5)
        hl = stand(hare(WHITE_C, 0.95), XL - 1.3, -2.1)
        hr = stand(hare(WHITE_C, 0.95), XR - 1.3, -2.1)
        sl = T("on snow", 26, INK).move_to([XL, -2.75, 0])
        sr = T("on bare brown ground", 26, TEXT).move_to([XR, -2.75, 0])
        self.at("white coat")
        self.play(FadeIn(snow), FadeIn(gr), FadeIn(div), FadeIn(hl, shift=UP * 0.2), FadeIn(hr, shift=UP * 0.2),
                  FadeIn(sl), FadeIn(sr), run_time=0.9)

        head = T("camouflage", 46, BLUE, font=TITLE_FONT).move_to([0, 3.2, 0])
        self.at("is camouflage")
        self.play(FadeIn(head, scale=0.9), run_time=0.6)
        sub = T("coloring that helps an animal blend in with its background", 26, TEXT).move_to([0, 2.6, 0])
        self.at("coloring that helps")
        self.play(FadeIn(sub), run_time=0.6)

        hx = hl.get_right()[0] - 0.55
        pl = bchip("predator", PURPLE, 26).move_to([hx, 1.85, 0])
        al = arr([hx, 1.52, 0], [hx, 0.85, 0], PURPLE)
        self.at("On snow")
        self.play(FadeIn(pl, shift=DOWN * 0.15), GrowArrow(al), run_time=0.6)
        helps = bchip("helps hide", GREEN, 28).move_to([XL + 1.75, -0.5, 0])
        self.at("helps hide")
        self.play(FadeIn(helps, shift=LEFT * 0.15), run_time=0.5)
        inv = T("not invisible", 26, GREY).next_to(helps, DOWN, buff=0.25)
        self.at("does not make")
        self.play(FadeIn(inv), run_time=0.5)

        hx2 = hr.get_right()[0] - 0.55
        pr = bchip("predator", PURPLE, 26).move_to([hx2, 1.85, 0])
        ar = arr([hx2, 1.52, 0], [hx2, 0.85, 0], PURPLE)
        self.at("On bare brown ground")
        self.play(FadeIn(pr, shift=DOWN * 0.15), GrowArrow(ar), run_time=0.6)
        costs = bchip("stands out", RED, 28).move_to([XR + 1.75, -0.5, 0])
        self.at("stands out")
        self.play(FadeIn(costs, shift=LEFT * 0.15), Indicate(hr, color=RED, scale_factor=1.04), run_time=0.7)

        to = T("trade-off", 46, YELLOW, font=TITLE_FONT).move_to([0, 3.2, 0])
        self.at("That is a")
        self.play(FadeOut(head), FadeOut(sub), FadeIn(to, scale=0.9), run_time=0.6)
        defn = T("a trait helps in one way but costs in another", 26, TEXT).move_to([0, 2.6, 0])
        self.at("means a trait")
        self.play(FadeIn(defn), run_time=0.5)
        self.at("helps in one way")
        self.play(Indicate(helps, color=GREEN, scale_factor=1.15), run_time=0.8)
        self.at("costs in another")
        self.play(Indicate(costs, color=RED, scale_factor=1.15), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Variation(SpokenScene):
    """four hares turn white at different times (variation) -> one hare cannot decide -> population over generations."""

    def construct(self):
        feet = -1.1
        xs = [-4.6, -1.55, 1.55, 4.6]
        hs = [stand(hare(BROWN_C, 0.78), x, feet) for x in xs]
        base = Line([-6.2, feet, 0], [6.2, feet, 0], color=GREY, stroke_width=3)
        tl = arr([-5.8, -2.6, 0], [5.8, -2.6, 0], GREY, w=4)
        tl_l = T("time", 26, GREY).move_to([5.2, -3.05, 0])
        lab = T("snowshoe hares in one forest", 32, TEXT).move_to([0, 2.5, 0])
        self.at("in one forest")
        self.play(FadeIn(base), *[FadeIn(h, shift=UP * 0.2) for h in hs], FadeIn(lab), GrowArrow(tl), FadeIn(tl_l),
                  run_time=0.9)

        self.at("white earlier")
        t1 = T("earlier", 28, YELLOW).move_to([xs[0], -1.7, 0])
        self.play(recoat(hs[0], WHITE_C), FadeIn(t1), run_time=0.8)
        self.at("than others")
        self.play(recoat(hs[1], WHITE_C), run_time=0.7)
        self.play(recoat(hs[2], WHITE_C), run_time=0.7)
        t4 = T("later", 28, YELLOW).move_to([xs[3], -1.7, 0])
        self.play(recoat(hs[3], WHITE_C), FadeIn(t4), run_time=0.7)

        var = bchip("variation", PURPLE, 42).move_to([0, 2.5, 0])
        self.at("called variation")
        self.play(ReplacementTransform(lab, var), run_time=0.7)

        self.at("cannot decide")
        keep = hs[1]
        self.play(FadeOut(VGroup(hs[0], hs[2], hs[3], t1, t4, tl, tl_l, base, var)),
                  keep.animate.scale(1.7).move_to([-3.0, -0.2, 0]), run_time=0.9)
        dec = bchip("cannot choose its color", RED, 30).move_to([3.5, 0.6, 0])
        self.at("decide to change")
        self.play(FadeIn(dec, shift=LEFT * 0.2), run_time=0.5)
        one = T("one hare", 28, GREY).next_to(keep, DOWN, buff=0.2)
        self.add(one)

        self.at("Change happens")
        self.play(FadeOut(VGroup(keep, one, dec)), run_time=0.6)
        pop_t = T("population", 40, YELLOW).move_to([0, 3.2, 0])
        sub = T("all the members of one species in one area", 26, TEXT).move_to([0, 2.65, 0])
        bl = RoundedRectangle(corner_radius=0.2, width=4.9, height=3.6, stroke_color=YELLOW, stroke_width=3
                              ).move_to([-3.6, 0.2, 0])
        br = RoundedRectangle(corner_radius=0.2, width=4.9, height=3.6, stroke_color=YELLOW, stroke_width=3
                              ).move_to([3.6, 0.2, 0])

        def grid(cx, fits):
            g = VGroup()
            for i in range(8):
                r, c = divmod(i, 4)
                h = hare(WHITE_C, 0.3, edge=GREEN if i in fits else EDGE)
                stand(h, cx - 1.65 + c * 1.1, -1.1 + (1 - r) * 1.7)
                g.add(h)
            return g
        left = grid(-3.6, {0, 5})
        right = grid(3.6, {0, 1, 3, 4, 5, 6})
        self.at("a population")
        self.play(FadeIn(pop_t), FadeIn(sub), Create(bl), run_time=0.7)
        self.play(FadeIn(left, lag_ratio=0.1), run_time=0.8)
        fit_c = bchip("timing fits the snow", GREEN, 26).move_to([-3.6, -2.25, 0])
        self.at("timing fits the snow")
        self.play(FadeIn(fit_c, shift=UP * 0.15),
                  *[Indicate(left[i], color=GREEN, scale_factor=1.15) for i in (0, 5)], run_time=0.9)
        self.at("more young")
        ar = arr([-0.85, 0.2, 0], [0.85, 0.2, 0], YELLOW, w=7)
        self.play(GrowArrow(ar), run_time=0.5)
        gen = VGroup(T("many", 26, YELLOW), T("generations", 26, YELLOW)).arrange(DOWN, buff=0.08).move_to([0, 0.95, 0])
        self.at("many generations")
        self.play(FadeIn(gen), Create(br), run_time=0.6)
        self.play(FadeIn(right, lag_ratio=0.1), run_time=0.8)
        self.at("more common")
        mc = bchip("more common", GREEN, 26).move_to([3.6, -2.25, 0])
        note = T("a sketch with made-up counts", 22, GREY).move_to([0, -3.15, 0])
        self.play(FadeIn(mc, shift=UP * 0.15), FadeIn(note), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    """the question answered: stands out, predators spot it more easily; one hare cannot choose; populations change."""

    def construct(self):
        qt = T("What happens to a white hare when the snow melts early?", 28, YELLOW).move_to([0, 3.3, 0])
        ground = band(0, -1.9, -3.5, 12.6, GROUND_C)
        h = stand(hare(WHITE_C, 1.3), -2.2, -1.9)
        place = T("bare brown ground", 28, TEXT).move_to([0, -2.7, 0])
        self.at("what happens to a white")
        self.play(FadeIn(ground), FadeIn(h, shift=UP * 0.2), FadeIn(place), Write(qt), run_time=1.0)

        so = bchip("stands out", RED, 34).move_to([3.7, 1.3, 0])
        self.at("stands out")
        self.play(FadeIn(so, shift=LEFT * 0.2), Indicate(h, color=RED, scale_factor=1.04), run_time=0.8)

        hx = h.get_right()[0] - 0.7
        pl = bchip("predator", PURPLE, 28).move_to([hx, 2.5, 0])
        ap = arr([hx, 2.17, 0], [hx, 1.45, 0], PURPLE)
        self.at("Predators can spot")
        self.play(FadeIn(pl, shift=DOWN * 0.15), GrowArrow(ap), run_time=0.6)
        sp = T("spotted more easily", 30, RED).move_to([3.7, 0.4, 0])
        self.at("more easily")
        self.play(FadeIn(sp, shift=UP * 0.1), run_time=0.5)

        self.at("cannot choose")
        nc = bchip("cannot choose a new coat", RED, 28).move_to([3.55, -0.9, 0])
        self.play(FadeIn(nc, shift=LEFT * 0.2), run_time=0.5)

        self.at("Only populations")
        self.play(FadeOut(VGroup(ground, h, place, qt, so, pl, ap, sp, nc)), run_time=0.6)
        pop = bchip("population", YELLOW, 52).move_to([0, 0.7, 0])
        gen = T("changes over many generations", 38, TEXT).move_to([0, -0.7, 0])
        self.play(FadeIn(pop, scale=0.9), run_time=0.5)
        self.at("over many generations")
        self.play(FadeIn(gen), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Only populations change, over many generations."
