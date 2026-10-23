"""Restoring ecosystems: people can help a damaged ecosystem come back  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  YELLOW = eagles, eagle pairs, eggs
  RED    = harm (DDT, DDE, habitat loss, cracked and failed eggs, new dangers)
  GREEN  = people's helping actions and recovery (ban, laws, protected places, eelgrass growing)
  BLUE   = water (the bay)
  GOLD   = limits and cautions (partial, slow, different)
  TEAL   = a vocabulary word, shown the moment it is spoken
  GREY   = axes, outlines, the sea floor, nests, de-emphasized
"""
import numpy as np
from bp_style import *  # noqa: F401,F403


def term(text, size=28):
    return chip(text, TEAL, size=size)


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def backed(mob, pad=0.12):
    back = Rectangle(width=mob.width + 2 * pad, height=mob.height + pad, stroke_width=0,
                     fill_color=BG, fill_opacity=1).move_to(mob)
    return VGroup(back, mob)


def pair_icon(scale=1.0):
    nest = RoundedRectangle(corner_radius=0.12, width=1.1, height=0.26, stroke_color=GREY, stroke_width=3,
                            fill_color=GREY, fill_opacity=0.4)
    a = Circle(radius=0.2, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9)
    b = Circle(radius=0.2, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.9)
    a.next_to(nest, UP, buff=0.0).shift(LEFT * 0.25)
    b.next_to(nest, UP, buff=0.0).shift(RIGHT * 0.25)
    return VGroup(nest, a, b).scale(scale)


def egg(color=YELLOW, sw=14, h=2.6):
    e = Ellipse(width=h * 0.74, height=h, stroke_color=color, stroke_width=sw, fill_color=color, fill_opacity=0.1)
    return e


class S00Title(TitleCard):
    LESSON = "Helping Ecosystems Recover"
    TITLE = "People Can Help Nature Recover"


# ---------------------------------------------------------------------------------------------
class S01Count(SpokenScene):
    """two bars from the lesson's numbers; the question."""

    def construct(self):
        base_y, H = -2.2, 3.7
        head = T("Bald eagle pairs counted in Virginia", 30, GREY).to_edge(UP, buff=0.5)
        axis = Line([-6.0, base_y, 0], [6.0, base_y, 0], color=GREY, stroke_width=3)
        self.play(FadeIn(head), Create(axis), run_time=0.8)

        h1 = H * 33 / 1070
        bar1 = Rectangle(width=1.7, height=h1, stroke_color=YELLOW, stroke_width=2, fill_color=YELLOW,
                         fill_opacity=0.85).move_to([-3.6, base_y + h1 / 2, 0])
        l1 = M("33 pairs", 32, YELLOW).next_to(bar1, UP, buff=0.2)
        y1 = M("1977", 30, TEXT).next_to(axis, DOWN, buff=0.15).set_x(-3.6)
        self.at("survey found only")
        self.play(GrowFromEdge(bar1, DOWN), FadeIn(l1), FadeIn(y1), run_time=0.9)

        bar2 = Rectangle(width=1.7, height=H, stroke_color=YELLOW, stroke_width=2, fill_color=YELLOW,
                         fill_opacity=0.85).move_to([3.6, base_y + H / 2, 0])
        l2 = M("1,070 pairs", 32, YELLOW).next_to(bar2, UP, buff=0.2)
        y2 = M("2016", 30, TEXT).next_to(axis, DOWN, buff=0.15).set_x(3.6)
        self.at("larger search counted")
        self.play(GrowFromEdge(bar2, DOWN), run_time=1.6)
        self.play(FadeIn(l2), FadeIn(y2), run_time=0.4)

        icon = pair_icon(1.5).move_to([0, 0.5, 0])
        cap = T("pair = two adults and a nest", 26, YELLOW).next_to(icon, DOWN, buff=0.25)
        self.at("pair is two")
        self.play(FadeIn(icon, shift=UP * 0.1), FadeIn(cap), run_time=0.6)

        note = T("2016: a larger search, so not a perfect match", 24, GREY).next_to(y2, DOWN, buff=0.25)
        note.set_x(0)
        self.at("perfect match")
        self.play(FadeIn(note), run_time=0.5)

        q = VGroup(T("Can people help", 36, TEXT), T("a damaged", 36, TEXT), T("ecosystem", 36, TEXT),
                   T("come back?", 36, TEXT)).arrange(DOWN, buff=0.12).move_to([0, 0.7, 0])
        self.at("can people help")
        self.play(FadeOut(icon), FadeOut(cap), FadeIn(q, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S02Shell(SpokenScene):
    """pesticide -> DDT -> breaks down to DDE -> shells thin -> egg breaks / fails -> few young."""

    def construct(self):
        t_pest = term("pesticide", 30).move_to([-4.2, 2.8, 0])
        self.at("pesticide is a chemical")
        self.play(FadeIn(t_pest, shift=DOWN * 0.1), run_time=0.5)
        sub = T("a chemical used to kill pests,\nsuch as insects", 24, TEAL).next_to(t_pest, DOWN, buff=0.15)
        sub.set_x(-3.9)
        self.play(FadeIn(sub), run_time=0.5)

        ddt = chip("DDT", RED, size=34).move_to([-4.4, 1.0, 0])
        self.at("common pesticide")
        self.play(FadeIn(ddt, scale=0.9), run_time=0.5)

        dde = chip("DDE", RED, size=34).move_to([-4.4, -1.4, 0])
        a1 = arr(ddt.get_bottom(), dde.get_top(), RED)
        al = T("breaks down", 26, RED).next_to(a1, RIGHT, buff=0.2)
        self.at("related chemical")
        self.play(GrowArrow(a1), FadeIn(al), run_time=0.6)
        self.play(FadeIn(dde, scale=0.9), run_time=0.5)

        e1 = egg(YELLOW, 14).move_to([0.9, -0.1, 0])
        e2 = egg(YELLOW, 14).move_to([4.2, -0.1, 0])
        elab = T("eagle egg: thick shell", 24, YELLOW).move_to([2.55, -2.1, 0])
        a2 = arr(dde.get_right() + RIGHT * 0.1, [-0.5, -1.4, 0], RED)
        self.at("make bird")
        self.play(FadeIn(e1), FadeIn(e2), FadeIn(elab), GrowArrow(a2), run_time=0.8)

        elab2 = T("eagle egg: thin shell", 24, RED).move_to([2.55, -2.1, 0])
        self.at("very thin")
        self.play(e1.animate.set_stroke(width=3), e2.animate.set_stroke(width=3), FadeOut(elab), FadeIn(elab2),
                  run_time=1.0)

        crack = VMobject(color=RED, stroke_width=6).set_points_as_corners(
            [e1.get_center() + np.array(p) for p in [(-0.8, 0.5, 0), (-0.3, 0.1, 0), (0.0, 0.6, 0),
                                                      (0.4, 0.0, 0), (0.9, 0.4, 0)]])
        broke = T("often broke", 30, RED).move_to([0.9, 2.0, 0])
        self.at("often broke")
        self.play(Create(crack), FadeIn(broke), run_time=0.7)

        xmark = VGroup(Line([-0.5, 0.5, 0], [0.5, -0.5, 0]), Line([-0.5, -0.5, 0], [0.5, 0.5, 0])).set_color(RED)
        xmark.set_stroke(width=8).move_to(e2.get_center())
        nohatch = T("failed to hatch", 30, RED).move_to([4.2, 2.0, 0])
        self.at("failed to hatch")
        self.play(Create(xmark), FadeIn(nohatch), run_time=0.7)

        few = T("few young eagles raised", 32, YELLOW, weight=BOLD).move_to([2.55, -3.1, 0])
        self.at("few young")
        self.play(FadeOut(elab2), FadeIn(few, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S03Act(SpokenScene):
    """other problems (red), what people did (green), habitat and conservation words."""

    def construct(self):
        h_l = T("Problems", 30, RED, weight=BOLD).move_to([-3.6, 3.0, 0])
        c1 = chip("DDT", RED, size=30).move_to([-3.6, 1.9, 0])
        self.play(FadeIn(h_l), FadeIn(c1), run_time=0.6)

        c2 = chip("habitat destroyed", RED, size=28).move_to([-3.6, 0.7, 0])
        self.at("destroyed eagle habitat")
        self.play(FadeIn(c2, scale=0.9), run_time=0.5)
        t_hab = term("habitat", 28).move_to([-3.6, -0.7, 0])
        d_hab = T("the place where eagles live", 24, TEAL).next_to(t_hab, DOWN, buff=0.15)
        self.at("place where eagles live")
        self.play(FadeIn(t_hab, shift=DOWN * 0.1), FadeIn(d_hab), run_time=0.6)

        h_r = T("People acted", 30, GREEN, weight=BOLD).move_to([3.2, 3.0, 0])
        self.at("people acted")
        self.play(FadeIn(h_r), run_time=0.5)
        g1 = chip("United States, 1972:\nmost DDT uses banned", GREEN, size=26).move_to([3.2, 1.7, 0])
        self.at("banned most uses")
        self.play(FadeIn(g1, shift=LEFT * 0.2), c1[0].animate.set_stroke(opacity=0.35), run_time=0.6)
        g2 = chip("Laws protect eagles\nand their nests", GREEN, size=26).move_to([3.2, 0.1, 0])
        self.at("laws protected")
        self.play(FadeIn(g2, shift=LEFT * 0.2), run_time=0.6)
        g3 = chip("Nesting places\nprotected", GREEN, size=26).move_to([3.2, -1.5, 0])
        self.at("protected the places")
        self.play(FadeIn(g3, shift=LEFT * 0.2), run_time=0.6)

        t_con = term("conservation", 30)
        d_con = T("protecting living things and their habitats so they last", 24, TEAL)
        grp = VGroup(t_con, d_con).arrange(DOWN, buff=0.15).move_to([0, -3.0, 0])
        self.at("called conservation")
        self.play(FadeIn(grp, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S04Decades(SpokenScene):
    """timeline 1972 -> 2016 from the lesson's years; young -> pair -> young loop; new dangers."""

    def construct(self):
        x0, x1 = -5.5, 5.5      # 1970 .. 2020
        px = lambda yr: x0 + (yr - 1970) * (x1 - x0) / 50.0
        ay = 1.6
        axis = Arrow([x0 - 0.3, ay, 0], [x1 + 0.4, ay, 0], buff=0, color=GREY, stroke_width=4, tip_length=0.25)
        self.at("took decades")
        self.play(Create(axis), run_time=0.4)
        m72 = Dot([px(1972), ay, 0], color=GREEN, radius=0.13)
        l72 = T("1972: DDT ban", 26, GREEN).next_to(m72, UP, buff=0.2).shift(RIGHT * 0.6)
        m77 = Dot([px(1977), ay, 0], color=YELLOW, radius=0.13)
        l77 = M("1977: 33 pairs", 24, YELLOW).next_to(m77, DOWN, buff=0.2).shift(LEFT * 0.0)
        m16 = Dot([px(2016), ay, 0], color=YELLOW, radius=0.13)
        l16 = M("2016: 1,070 pairs", 24, YELLOW).next_to(m16, DOWN, buff=0.2).shift(LEFT * 0.4)
        span = Line([px(1972), ay + 1.1, 0], [px(2016), ay + 1.1, 0], color=GREEN, stroke_width=4)
        dec = backed(T("decades", 30, GREEN, weight=BOLD)).move_to(span.get_center())
        self.play(FadeIn(m72), FadeIn(l72), FadeIn(m77), FadeIn(l77), run_time=0.4)
        self.play(Create(span), FadeIn(dec), FadeIn(m16), FadeIn(l16), run_time=0.6)

        ry = -0.9
        y1 = chip("young eagle", YELLOW, size=28).move_to([-4.6, ry, 0])
        self.at("young eagles take")
        self.play(FadeIn(y1), run_time=0.5)
        pr = VGroup(pair_icon(1.0), T("pair", 26, YELLOW)).arrange(DOWN, buff=0.12).move_to([0, ry, 0])
        a1 = arr([-3.2, ry, 0], [-1.0, ry, 0], YELLOW)
        al1 = T("several years", 26, YELLOW).next_to(a1, UP, buff=0.12)
        self.at("several years")
        self.play(GrowArrow(a1), FadeIn(al1), run_time=0.6)
        self.at("old enough")
        self.play(FadeIn(pr, scale=0.9), run_time=0.5)
        y2 = chip("more young", YELLOW, size=28).move_to([4.6, ry, 0])
        a2 = arr([1.0, ry, 0], [3.0, ry, 0], YELLOW)
        al2 = T("raise young", 26, YELLOW).next_to(a2, UP, buff=0.12)
        self.at("raise young")
        self.play(GrowArrow(a2), FadeIn(al2), FadeIn(y2), run_time=0.7)
        back = CurvedArrow(y2.get_bottom() + DOWN * 0.05, pr.get_bottom() + DOWN * 0.05, angle=-TAU / 4.2,
                           color=YELLOW, stroke_width=5)
        bl = T("grow into pairs too", 26, YELLOW).move_to([2.3, -2.75, 0])
        self.at("those young become")
        self.play(Create(back), FadeIn(bl), run_time=0.9)

        dan = chip("eagles also die, face new dangers", RED, size=24).move_to([-3.3, -2.6, 0])
        self.at("also die")
        self.play(FadeIn(dan, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S05Grass(SpokenScene):
    """a bay floor: eelgrass gone, seeds by hand in a plot, plants spread past the plot."""

    def construct(self):
        floor_y = -2.3
        water = Rectangle(width=12.4, height=4.9, stroke_width=0, fill_color=BLUE, fill_opacity=0.14)
        water.move_to([0, floor_y + 2.45, 0])
        floor = Rectangle(width=12.4, height=0.35, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                          fill_opacity=0.45).move_to([0, floor_y - 0.175, 0])
        lab = T("a coastal bay in Virginia", 24, BLUE).move_to([-3.9, 2.0, 0])
        self.add(water, floor, lab)
        note = T("schematic, not to scale", 24, GREY).move_to([0, -3.0, 0])
        self.add(note)
        wave = Line(LEFT, RIGHT)

        def wave_up(m, dt=0):
            t = self.elapsed()
            pts = [[x, floor_y + 4.85 + 0.07 * np.sin(1.3 * x + 2.2 * t), 0] for x in np.linspace(-6.2, 6.2, 60)]
            m.become(VMobject(color=BLUE, stroke_width=4).set_points_smoothly(pts))
        wave.add_updater(wave_up)
        self.add(wave)

        t_res = term("restoration", 30).move_to([3.9, 1.85, 0])
        d_res = T("helping a damaged\necosystem recover", 24, TEAL).next_to(t_res, DOWN, buff=0.12)
        self.at("restoration is helping")
        self.play(FadeIn(t_res, shift=DOWN * 0.1), FadeIn(d_res), run_time=0.6)

        def blades(xs, hmax=1.7, seed=0):
            rng = np.random.RandomState(seed)
            out = VGroup()
            for x in xs:
                h = hmax * (0.6 + 0.4 * rng.rand())
                out.add(Line([x, floor_y, 0], [x + 0.12 * (rng.rand() - 0.5), floor_y + h, 0], color=GREEN,
                             stroke_width=5))
            return out

        old = blades(np.arange(-5.6, 5.7, 0.4), 1.7, 1)
        self.at("wiped out")
        self.play(Create(old), run_time=0.5)
        gone = T("1933: eelgrass gone (disease and a hurricane)", 26, RED).move_to([0, 0.6, 0])
        self.play(FadeOut(old), FadeIn(gone), run_time=0.9)

        plot = DashedVMobject(Rectangle(width=3.6, height=2.5, color=TEXT, stroke_width=3), num_dashes=40)
        plot.move_to([-3.2, floor_y + 1.25, 0])
        plab = T("planted area", 24, TEXT).next_to(plot, UP, buff=0.12)
        seeds = VGroup(*[Dot([-4.7 + 0.4 * i, 0.9 + 0.15 * (i % 2), 0], radius=0.07, color=GREEN) for i in range(8)])
        self.at("spread eelgrass seeds")
        self.play(FadeOut(gone), Create(plot), FadeIn(plab), run_time=0.6)
        by = T("seeds scattered by hand", 26, GREEN).move_to([-3.0, 0.9, 0]) if False else None
        self.play(FadeIn(seeds), run_time=0.3)
        self.play(seeds.animate.shift(DOWN * 2.9), run_time=1.0, rate_func=smooth)
        self.play(FadeOut(seeds), run_time=0.2)

        new_in = blades(np.arange(-4.9, -1.6, 0.35), 1.6, 2)
        self.at("new plants made")
        self.play(Create(new_in), run_time=0.9)
        new_out = blades(np.arange(-0.6, 5.7, 0.4), 1.6, 3)
        arrw = arr([-1.3, floor_y + 1.2, 0], [-0.1, floor_y + 1.2, 0], GREEN)
        self.at("past the planted")
        self.play(GrowArrow(arrw), Create(new_out), run_time=1.4)

        big = VGroup(T("3,612", 44, GREEN, weight=BOLD), T("hectares of eelgrass", 30, GREEN),
                     T("2020 study", 24, GREY)).arrange(DOWN, buff=0.1).move_to([3.2, 0.9, 0])
        bb = backed(big, 0.18)
        self.at("study reported")
        self.play(FadeOut(t_res), FadeOut(d_res), FadeIn(bb, shift=UP * 0.1), run_time=0.7)
        self.finish()


# ---------------------------------------------------------------------------------------------
class S06Answer(SpokenScene):
    """limits, then the answer."""

    def construct(self):
        head = T("Recovery has limits", 36, GOLD, weight=BOLD).move_to([0, 3.0, 0])
        self.play(FadeIn(head), run_time=0.5)
        c1 = chip("A review of 400 studies:\ndamaged places often improve", GREEN, size=28).move_to([0, 1.5, 0])
        self.at("review of")
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.6)
        c2 = chip("Full recovery: less common\n(while scientists watched)", GOLD, size=28).move_to([0, -0.3, 0])
        self.at("full recovery")
        self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.6)
        c3 = chip("A recovered place can look different", GOLD, size=28).move_to([0, -1.9, 0])
        self.at("look different")
        self.play(FadeIn(c3, shift=UP * 0.1), run_time=0.6)

        q = T("Can people help a damaged ecosystem come back?", 34, TEXT)
        fit(q, max_w=11.8)
        q.move_to([0, 3.0, 0])
        self.at("can people help")
        self.play(FadeOut(head), FadeOut(c1), FadeOut(c2), FadeOut(c3), run_time=0.5)
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.6)
        yes = T("Yes.", 60, GREEN, weight=BOLD).move_to([0, 1.6, 0])
        self.at("yes")
        self.play(FadeIn(yes, scale=0.8), run_time=0.5)
        r1 = chip("remove the cause", GREEN, size=30)
        r2 = chip("protect", GREEN, size=30)
        r3 = chip("restore", GREEN, size=30)
        row = VGroup(r1, r2, r3).arrange(RIGHT, buff=0.5).move_to([0, 0.2, 0])
        self.at("remove the cause")
        self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.4)
        self.at("protect and")
        self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.4)
        self.at("restore but")
        self.play(FadeIn(r3, shift=UP * 0.1), run_time=0.4)
        but = T("but recovery is often", 28, GOLD).move_to([0, -1.2, 0])
        g1, g2, g3 = (chip(w, GOLD, size=30) for w in ("slow", "partial", "different"))
        row2 = VGroup(g1, g2, g3).arrange(RIGHT, buff=0.5).move_to([0, -2.4, 0])
        self.at("often slow")
        self.play(FadeIn(but), run_time=0.4)
        self.play(FadeIn(g1, shift=UP * 0.1), run_time=0.3)
        self.play(FadeIn(g2, shift=UP * 0.1), run_time=0.3)
        self.play(FadeIn(g3, shift=UP * 0.1), run_time=0.3)
        self.finish()


class S07End(EndCard):
    LINE = "Remove the cause, protect, restore: recovery is slow, partial, different."
