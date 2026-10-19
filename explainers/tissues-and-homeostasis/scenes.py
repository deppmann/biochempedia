"""Tissues, organs and homeostasis: name the variable, then the loop  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = the regulated variable / the animal's own body value (core temperature, blood osmolality)
  ORANGE = the outside world (hot room air, the water around a fish or crab)
  TEAL   = the set point
  BLUE   = the sensor
  PURPLE = the integrator
  GREEN  = the effector and its response (sweating, shivering)
  RED    = a deviation of the variable (rises, falls)
  GOLD   = energy expenditure (mouse bars)
  GREY   = outlines, axes, de-emphasised text
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


# ---------------------------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------------------------
def bchip(text, color=BLUE, size=26, **kw):
    """chip with an opaque backing so lines drawn behind it do not show through."""
    c = chip(text, color, size=size, **kw)
    back = RoundedRectangle(corner_radius=0.14, width=c[0].width, height=c[0].height, stroke_width=0,
                            fill_color=BG, fill_opacity=1).move_to(c[0])
    return VGroup(back, *c)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def elbow(pts, color=GREY, w=5):
    """polyline with an arrowhead on the last segment."""
    pts = [np.array(p, float) for p in pts]
    g = VGroup()
    for a, b in zip(pts[:-2], pts[1:-1]):
        g.add(Line(a, b, color=color, stroke_width=w))
    g.add(Arrow(pts[-2], pts[-1], buff=0, color=color, stroke_width=w, tip_length=0.22,
                max_tip_length_to_length_ratio=0.9, max_stroke_width_to_length_ratio=12))
    return g


def axes_box(origin, w, h, color=GREY):
    ox, oy = origin
    return VGroup(Arrow([ox, oy, 0], [ox + w, oy, 0], buff=0, color=color, stroke_width=4, tip_length=0.18),
                  Arrow([ox, oy, 0], [ox, oy + h, 0], buff=0, color=color, stroke_width=4, tip_length=0.18))


class S00Title(TitleCard):
    LESSON = "Tissues, organs and homeostasis"
    TITLE = "Name the variable, then the loop"

    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        title = T(self.TITLE, size=54, font=TITLE_FONT)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        g = VGroup(brand, lesson, title, rule).arrange(DOWN, buff=0.32)
        self.play(FadeIn(g), run_time=self.beat(0.2))
        self.wait(self.beat(0.55))
        self.play(FadeOut(g), run_time=self.beat(0.2))
        self.finish()


# ---------------------------------------------------------------------------------------------
class S01Room(SpokenScene):
    """Hot room: the egg's level climbs to the air; Blagden's tongue thermometer stays near 98 F."""

    def construct(self):
        base, top = -2.3, 1.9          # tube bottom and the air level (about 200 F)
        scale = (top - base) / 200.0   # drawn from 0 F at the bottom of the tube
        tw = 1.2
        xe, xp = -3.7, 1.3

        self.at("Charles")
        air = DashedLine([-5.3, top, 0], [5.3, top, 0], color=ORANGE, stroke_width=5, dash_length=0.2)
        air_lbl = T("air in the room: about 200 °F", 28, ORANGE).move_to([0, top + 0.5, 0])
        tubes = VGroup(*[RoundedRectangle(corner_radius=0.1, width=tw, height=top - base, stroke_color=GREY,
                                          stroke_width=3).move_to([x, (top + base) / 2, 0]) for x in (xe, xp)])
        lbl_e = T("an egg", 28, TEXT).move_to([xe, base - 0.75, 0])
        lbl_p = T("Blagden, under the tongue", 26, TEXT).move_to([xp, base - 0.75, 0])
        note = T("drawn from 0 °F, egg start not given", 22, GREY).to_edge(DOWN, buff=0.25)
        self.play(Create(air), FadeIn(air_lbl), FadeIn(tubes), FadeIn(lbl_e), FadeIn(lbl_p), run_time=1.2)

        he, hp = ValueTracker(0.01), ValueTracker(0.01)
        fe = always_redraw(lambda: Rectangle(width=tw - 0.16, height=he.get_value(), stroke_width=0,
                                             fill_color=ORANGE, fill_opacity=0.85).move_to(
            [xe, base + he.get_value() / 2, 0]))
        fp = always_redraw(lambda: Rectangle(width=tw - 0.16, height=hp.get_value(), stroke_width=0,
                                             fill_color=YELLOW, fill_opacity=0.85).move_to(
            [xp, base + hp.get_value() / 2, 0]))
        self.add(fe, fp)
        self.at("A thermometer under")
        v98 = VGroup(T("98 °F", 32, YELLOW, weight=BOLD), T("about 1 °F above his usual", 24, YELLOW)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        v98.move_to([xp + tw / 2 + 0.3 + v98.width / 2, base + 98 * scale, 0])
        self.play(hp.animate.set_value(98 * scale), run_time=3.0, rate_func=smooth)
        self.play(FadeIn(v98), run_time=0.5)
        self.at("An egg in hot air")
        self.play(he.animate.set_value(top - base), run_time=max(2.5, self.t_of("A living person did not") - 0.7 - self.elapsed()), rate_func=smooth)
        self.at("A living person did not")
        self.play(Indicate(VGroup(tubes[1], fp), color=YELLOW, scale_factor=1.06), FadeIn(note), run_time=1.2)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Loop(SpokenScene):
    """Five parts of any homeostatic loop, built into a closed loop with a dot travelling round it."""

    def construct(self):
        V = bchip("regulated variable", YELLOW, 26).move_to([-4.3, 0.1, 0])
        S = bchip("sensor", BLUE, 28).move_to([-1.4, 2.4, 0])
        I = bchip("integrator", PURPLE, 28).move_to([2.2, 2.4, 0])
        SP = bchip("set point", TEAL, 28).move_to([5.1, 2.4, 0])
        E = bchip("effector", GREEN, 28).move_to([2.2, -2.4, 0])
        a_vs = arr(V.get_top() + UP * 0.0 + RIGHT * 0.6, S.get_left(), GREY)
        a_si = arr(S.get_right(), I.get_left(), GREY)
        a_spi = arr(SP.get_left(), I.get_right(), TEAL)
        a_ie = arr(I.get_bottom(), E.get_top(), GREY)
        a_ev = arr(E.get_left(), V.get_bottom() + RIGHT * 0.7, GREY)
        mid_lines = [T(x, 24, GREY) for x in ("homeostasis:", "holding a body variable", "within a range compatible", "with staying alive")]
        mid = VGroup(*mid_lines).arrange(DOWN, buff=0.12)
        mid.move_to([-0.1, 0.4, 0])

        self.at("Biologists call this homeostasis")
        self.play(FadeIn(mid_lines[0], scale=1.1), run_time=0.6)
        self.at("the holding of a body variable")
        self.play(FadeIn(mid_lines[1]), run_time=0.6)
        self.at("within a range")
        self.play(FadeIn(mid_lines[2]), run_time=0.6)
        self.at("staying alive")
        self.play(FadeIn(mid_lines[3]), run_time=0.6)
        self.at("Every loop")
        self.at("regulated variable")
        self.play(FadeIn(V, scale=0.9), run_time=0.6)
        self.at("setpoint is its")
        self.play(FadeIn(SP, scale=0.9), run_time=0.6)
        self.at("The sensor measures")
        self.play(GrowArrow(a_vs), FadeIn(S, scale=0.9), run_time=0.7)
        self.at("the integrator compares")
        self.play(GrowArrow(a_si), FadeIn(I, scale=0.9), run_time=0.6)
        self.play(GrowArrow(a_spi), run_time=0.5)
        self.at("The effector")
        self.play(GrowArrow(a_ie), FadeIn(E, scale=0.9), run_time=0.7)
        self.at("changes the variable")
        self.play(GrowArrow(a_ev), run_time=0.6)
        path = VMobject().set_points_as_corners([
            V.get_top() + RIGHT * 0.6, S.get_left(), S.get_right(), I.get_left(), I.get_bottom(), E.get_top(),
            E.get_left(), V.get_bottom() + RIGHT * 0.7])
        dot = Dot(path.get_start(), radius=0.15, color=YELLOW)
        self.play(FadeIn(dot), run_time=0.2)
        self.play(MoveAlongPath(dot, path), run_time=max(1.5, self.narration_s + 0.3 - self.elapsed() - 0.4),
                  rate_func=linear)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Human(SpokenScene):
    """The loop for core temperature in an adult human, with the two effector branches."""

    def construct(self):
        V = bchip("variable:\ncore temperature", YELLOW, 24).move_to([-4.4, 2.1, 0])
        S = bchip("sensors:\nskin and brain\nnerve cells", BLUE, 24).move_to([-0.6, 2.1, 0])
        I = bchip("integrator:\nhypothalamus", PURPLE, 24).move_to([3.7, 2.1, 0])
        E1 = bchip("effector:\nsweat glands", GREEN, 24).move_to([3.9, 0.0, 0])
        E2 = bchip("effector:\nskeletal muscles", GREEN, 24).move_to([3.9, -2.2, 0])
        a_vs = arr(V.get_right(), S.get_left())
        a_si = arr(S.get_right(), I.get_left())
        a_ie1 = arr(I.get_bottom(), E1.get_top())
        a_ie2 = elbow([I.get_right(), [6.0, I.get_center()[1], 0], [6.0, E2.get_center()[1], 0], E2.get_right()])
        t1 = VGroup(T("when temperature rises:", 24, RED), T("evaporation of sweat removes heat", 24, TEXT)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        t2 = VGroup(T("when it falls:", 24, RED), T("they shiver and release heat", 24, TEXT)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        t1.next_to(E1, LEFT, buff=0.9).align_to(E1, UP).shift(DOWN * 0.1)
        t2.next_to(E2, LEFT, buff=0.9).align_to(E2, UP).shift(DOWN * 0.1)
        b1 = arr(E1.get_left(), t1.get_right() + RIGHT * 0.0, GREEN)
        b2 = arr(E2.get_left(), t2.get_right() + RIGHT * 0.0, GREEN)
        adult = T("in an adult human", 24, GREY).move_to([-4.4, 1.05, 0])

        self.at("In an adult human")
        self.play(FadeIn(V, scale=0.9), FadeIn(adult), run_time=0.6)
        self.at("Temperature sensitive nerve cells")
        self.play(GrowArrow(a_vs), FadeIn(S, scale=0.9), run_time=0.7)
        self.at("The hypothalamus")
        self.play(GrowArrow(a_si), FadeIn(I, scale=0.9), run_time=0.7)
        self.at("When temperature rises")
        self.play(GrowArrow(a_ie1), FadeIn(E1, scale=0.9), run_time=0.6)
        self.at("evaporation of sweat")
        self.play(GrowArrow(b1), FadeIn(t1), run_time=0.8)
        self.at("When it falls")
        self.play(Create(a_ie2), FadeIn(E2, scale=0.9), run_time=0.9)
        self.at("shiver and release heat")
        self.play(GrowArrow(b2), FadeIn(t2), run_time=0.8)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Feedback(SpokenScene):
    """A dot (core temperature) is pushed back to the set point from above and from below; then the set point moves."""

    def construct(self):
        ax = Arrow([-5.4, -2.7, 0], [-5.4, 2.9, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.2)
        ax_lbl = T("core temperature", 24, YELLOW).next_to(ax, UP, buff=0.12).shift(RIGHT * 1.0)
        band = Rectangle(width=8.4, height=0.55, stroke_color=TEAL, stroke_width=2, fill_color=TEAL,
                         fill_opacity=0.3).move_to([-0.8, 0.0, 0])
        sp = T("set point", 28, TEAL).move_to([4.6, 0.0, 0])
        dot = Dot([-2.6, 0.0, 0], radius=0.26, color=YELLOW)
        self.play(Create(ax), FadeIn(ax_lbl), FadeIn(band), FadeIn(sp), FadeIn(dot), run_time=0.2)

        x = -2.6
        self.at("If temperature rises")
        up_lbl = T("rises", 26, RED).move_to([x - 1.1, 2.0, 0])
        self.play(dot.animate.move_to([x, 2.0, 0]).set_color(RED), FadeIn(up_lbl), run_time=0.8)
        self.at("sweating brings it down")
        a_dn = arr([x + 0.0, 1.45, 0], [x, 0.5, 0], GREEN, w=7)
        l_dn = T("sweating", 26, GREEN).move_to([x + 1.4, 1.1, 0])
        self.play(GrowArrow(a_dn), FadeIn(l_dn), run_time=0.5)
        self.play(dot.animate.move_to([x, 0, 0]).set_color(YELLOW), run_time=0.8)
        self.at("If it falls")
        self.play(FadeOut(up_lbl), FadeOut(a_dn), FadeOut(l_dn), run_time=0.3)
        dn_lbl = T("falls", 26, RED).move_to([x - 1.0, -2.0, 0])
        self.play(dot.animate.move_to([x, -2.0, 0]).set_color(RED), FadeIn(dn_lbl), run_time=0.8)
        self.at("shivering brings it up")
        a_up = arr([x, -1.45, 0], [x, -0.5, 0], GREEN, w=7)
        l_up = T("shivering", 26, GREEN).move_to([x + 1.5, -1.1, 0])
        self.play(GrowArrow(a_up), FadeIn(l_up), run_time=0.5)
        self.play(dot.animate.move_to([x, 0, 0]).set_color(YELLOW), run_time=0.8)
        self.at("Both are negative feedback")
        self.play(FadeOut(dn_lbl), FadeOut(a_up), FadeOut(l_up), run_time=0.3)
        neg = T("negative feedback: the response opposes the deviation", 26, TEXT).move_to([-0.3, -3.1, 0])
        self.play(FadeIn(neg), run_time=0.6)
        self.at("The set point itself can move")
        self.play(FadeOut(neg), run_time=0.3)
        self.play(band.animate.move_to([-0.8, 1.7, 0]), sp.animate.move_to([4.6, 1.7, 0]), run_time=1.2)
        self.at("In a fever")
        fv = T("fever: set point raised", 26, TEAL).move_to([4.2, 2.45, 0])
        self.play(FadeIn(fv), run_time=0.4)
        self.at("feels cold and shivers")
        cold = T("feels cold", 26, TEXT).move_to([x - 1.4, -0.0, 0])
        a_f = arr([x, 0.45, 0], [x, 1.2, 0], GREEN, w=7)
        l_f = T("shivers", 26, GREEN).move_to([x + 1.2, 0.8, 0])
        self.play(FadeIn(cold), GrowArrow(a_f), FadeIn(l_f), run_time=0.6)
        self.play(dot.animate.move_to([x, 1.7, 0]), run_time=1.0)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Conform(SpokenScene):
    """Two sketch plots: body temperature (regulator vs fish that follows the water) and the shore crab's blood."""

    def construct(self):
        w, h = 5.0, 4.0
        o1, o2 = (-5.7, -2.2), (1.0, -2.2)
        A1, A2 = axes_box(o1, w, h), axes_box(o2, w, h)
        x1 = T("outside temperature", 22, ORANGE).next_to(A1, DOWN, buff=0.12)
        y1 = T("body temperature", 24, YELLOW).move_to([o1[0] + 1.3, o1[1] + h + 0.45, 0])
        x2 = T("water salt concentration", 22, ORANGE).next_to(A2, DOWN, buff=0.12)
        y2 = T("blood osmolality", 24, YELLOW).move_to([o2[0] + 1.2, o2[1] + h + 0.45, 0])
        end_l = T("about half strength", 22, GREY).move_to([o2[0] + 1.0, o2[1] - 0.4, 0])
        end_r = T("full strength", 22, GREY).move_to([o2[0] + w - 0.75, o2[1] - 0.4, 0])
        note = T("in this sketch", 22, GREY).to_edge(DOWN, buff=0.15)

        def P(o, fx, fy):
            return [o[0] + fx * w, o[1] + fy * h, 0]

        tag_r = T("regulator: holds a variable fairly steady", 26, TEXT).move_to([0, 3.35, 0])
        tag_c = T("conformer: lets it follow the environment", 26, TEXT).move_to([0, 2.85, 0])
        self.at("A regulator holds")
        self.play(Create(A1), FadeIn(x1), FadeIn(y1), FadeIn(note), FadeIn(tag_r), run_time=1.0)
        self.at("a conformer")
        self.play(FadeIn(tag_c), run_time=0.6)
        self.at("An adult human regulates")
        human = Line(P(o1, 0.05, 0.62), P(o1, 0.95, 0.62), color=YELLOW, stroke_width=7)
        hl = T("adult human", 24, YELLOW).move_to(P(o1, 0.5, 0.74))
        self.play(Create(human), FadeIn(hl), run_time=0.9)
        self.at("A typical teleost fish")
        fish = Line(P(o1, 0.05, 0.12), P(o1, 0.95, 0.5), color=YELLOW, stroke_width=7)
        fl = T("lake teleost fish", 24, YELLOW).move_to(P(o1, 0.62, 0.11))
        self.play(Create(fish), FadeIn(fl), run_time=1.0)
        self.at("different solution")
        self.wait(0.3)
        self.at("The shore crab")
        self.play(Create(A2), FadeIn(x2.next_to(A2, DOWN, buff=0.78)), FadeIn(y2), FadeIn(end_l), FadeIn(end_r), run_time=1.0)
        self.at("conforms in full")
        water = DashedLine(P(o2, 0.05, 0.05), P(o2, 0.95, 0.95), color=ORANGE, stroke_width=5, dash_length=0.18)
        wl = T("the water", 24, ORANGE).move_to(P(o2, 0.62, 0.3))
        crab_r = Line(P(o2, 0.62, 0.62), P(o2, 0.95, 0.95), color=YELLOW, stroke_width=7)
        self.play(Create(water), FadeIn(wl), run_time=0.8)
        self.play(Create(crab_r), run_time=0.7)
        self.at("regulates in diluted")
        crab_l = Line(P(o2, 0.05, 0.62), P(o2, 0.62, 0.62), color=YELLOW, stroke_width=7)
        cl = T("shore crab blood", 24, YELLOW).move_to(P(o2, 0.3, 0.74))
        self.play(Create(crab_l), FadeIn(cl), run_time=0.9)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Cost(SpokenScene):
    """Mouse energy expenditure bars (ratio about 1.3), then the rule to keep."""

    def construct(self):
        head = T("energy expenditure of single-housed male mice, one laboratory strain", 26, GREY).move_to([0, 2.8, 0])
        x0, L = -2.6, 3.8
        b30 = Rectangle(width=L, height=1.1, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.45
                        ).move_to([x0 + L / 2, 1.0, 0])
        b22 = Rectangle(width=L * 1.3, height=1.1, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.45
                        ).move_to([x0 + L * 1.3 / 2, -0.4, 0])
        l30 = T("at 30 °C", 28, TEXT).next_to(b30, LEFT, buff=0.3)
        l22 = T("at 22 °C", 28, TEXT).next_to(b22, LEFT, buff=0.3)
        guide = DashedLine([x0 + L, 1.6, 0], [x0 + L, -0.95, 0], color=GREY, stroke_width=3)
        pct = T("about 30% higher", 28, GOLD)
        pct.move_to([x0 + L * 1.3 + 0.3 + pct.width / 2, -0.4, 0])
        why = T("a small body loses heat fast", 28, TEXT).move_to([0.2, -2.0, 0])

        self.at("Regulation is not free")
        intro = T("regulation is not free", 44, font=TITLE_FONT).move_to([0, 0.3, 0])
        self.play(FadeIn(intro, shift=UP * 0.15), run_time=0.7)
        self.at("In single")
        self.play(FadeOut(intro), FadeIn(head), run_time=0.6)
        self.at("energy expenditure")
        self.play(FadeIn(l30), GrowFromEdge(b30, LEFT), run_time=0.9)
        self.play(FadeIn(l22), GrowFromEdge(b22, LEFT), run_time=1.1)
        self.at("higher at")
        self.play(Create(guide), FadeIn(pct), run_time=0.8)
        self.at("A mouse is small")
        self.play(FadeIn(why), run_time=0.6)
        self.at("Name the variable first")
        self.play(*[FadeOut(m) for m in (head, b30, b22, l30, l22, guide, pct, why)], run_time=0.6)
        c1 = chip("name the variable first", YELLOW, 34)
        c2 = chip("then the loop that holds it", GREY, 34)
        a = arr(c1.get_right(), c2.get_left(), GREY)
        grp = VGroup(c1, c2).arrange(RIGHT, buff=1.1)
        fit(grp)
        a = arr(c1.get_right(), c2.get_left(), GREY)
        self.play(FadeIn(c1, scale=0.9), run_time=0.6)
        self.at("the loop that holds it")
        self.play(GrowArrow(a), FadeIn(c2, scale=0.9), run_time=0.7)
        self.finish()


class S07End(EndCard):
    LINE = "Name the variable first, then the loop that holds it."
