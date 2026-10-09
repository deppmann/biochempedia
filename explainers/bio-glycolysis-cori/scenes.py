"""Carl Cori & Gerty Cori: scientist profile video (Biochemistrypedia, glycolysis lesson)

The portrait (public/scientists/cori.png, an AI-generated engraving-style illustration from
The Molecule Hunters) is the anchor: the title scene pushes in on it, then it stays as a framed
inset on the left while the right side animates the story's beats as the narrator reaches them.
Every cue is a self.at("spoken words") lookup in audio/words.json (word timestamps of the real audio).
Nothing on screen adds a fact that is not in the lesson entry (name, dates, contribution, story, quotes).

COLOR MAP (one color per concept, whole video)
  GOLD   = the Coris, the portrait frame, recognition (Nobel, full professorship, "she refused", "accurate")
  YELLOW = years / dates, the sixteen years
  TEAL   = places and institutions (Prague, United States, Buffalo, Washington University)
  RED    = obstacles and harm (the director's order, the salary gap, nepotism rules, broken enzyme, disease)
  BLUE   = enzymes (phosphorylase, debranching enzyme, the missing enzyme)
  GREEN  = glucose and glycogen ("free glucose", wrong-shaped glycogen)
  AMBER  = the discarded supernatant fraction
  GREY   = structure, labels, Carl's salary bar
"""
import os
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

config.disable_caching = True

AMBER = "#E0A458"
CX = 1.9            # centre of the content area to the right of the portrait column
PORT_X = -4.7       # portrait column centre
PORT_H = 3.4
PORT_Y = 1.1
IMG = Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent / "cori_crop.png"
NAME = "Carl Cori & Gerty Cori"
DATES = "1896–1984 · 1896–1957"
CAPTION = "illustration · AI-generated"


def portrait(height=PORT_H, center=(PORT_X, PORT_Y)):
    img = ImageMobject(str(IMG))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["cubic"])
    img.set_height(height)
    img.move_to([center[0], center[1], 0])
    border = Rectangle(width=img.width, height=img.height, stroke_color=GOLD, stroke_width=3, fill_opacity=0)
    border.move_to(img)
    return img, border


def column_labels():
    """Caption, name and dates under the inset portrait."""
    cap = T(CAPTION, 22, GREY).move_to([PORT_X, PORT_Y - PORT_H / 2 - 0.32, 0])
    n1 = T("Carl Cori", 28, TEXT, font=TITLE_FONT)
    n2 = T("& Gerty Cori", 28, TEXT, font=TITLE_FONT)
    name = VGroup(n1, n2).arrange(DOWN, buff=0.1).move_to([PORT_X, PORT_Y - PORT_H / 2 - 1.2, 0])
    dates = T(DATES, 22, GOLD).move_to([PORT_X, PORT_Y - PORT_H / 2 - 1.95, 0])
    if dates.width > 3.2:
        dates.scale_to_fit_width(3.2)
    return cap, name, dates


class BioScene(SpokenScene):
    def add_column(self):
        img, border = portrait()
        cap, name, dates = column_labels()
        self.add(img, border, cap, name, dates)

    def chip_at(self, text, color, x, y, size=28, **kw):
        c = chip(text, color, size, **kw)
        c.move_to([x, y, 0])
        return c


class S00Title(BioScene):
    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA  ·  SCIENTIST PROFILE", 22, TEAL, weight=BOLD).move_to([0, 3.4, 0])
        # build the inset version, then scale it up to the opening size
        img, border = portrait()
        big_h = 4.0
        k = big_h / PORT_H
        big_c = np.array([0.0, 0.8, 0.0])
        for m in (img, border):
            m.scale(k, about_point=ORIGIN).move_to(big_c)
        cap = T(CAPTION, 22, GREY).move_to([0, 0.8 - big_h / 2 - 0.3, 0])
        name = T(NAME, 52, font=TITLE_FONT)
        fit(name, max_w=11.5)
        name.move_to([0, -2.5, 0])
        dates = T(DATES, 28, GOLD).move_to([0, -3.2, 0])
        rule = Line(LEFT * 1.0, RIGHT * 1.0, color=GOLD, stroke_width=4).move_to([0, -2.9, 0])

        self.play(FadeIn(img), FadeIn(border), FadeIn(brand), FadeIn(cap), run_time=0.4)
        # slow push-in while the name and dates arrive
        self.play(img.animate.scale(1.05), border.animate.scale(1.05),
                  Write(name, run_time=1.0), run_time=1.5, rate_func=linear)
        self.play(GrowFromCenter(rule), FadeIn(dates), run_time=0.35)
        # hand over to the inset layout used by every later scene
        cap2, name2, dates2 = column_labels()
        self.play(AnimationGroup(
            img.animate.scale(1 / (k * 1.05)).move_to([PORT_X, PORT_Y, 0]),
            border.animate.scale(1 / (k * 1.05)).move_to([PORT_X, PORT_Y, 0]),
            cap.animate.move_to(cap2),
            Succession(AnimationGroup(FadeOut(name), FadeOut(dates), FadeOut(rule), FadeOut(brand)),
                       AnimationGroup(FadeIn(name2), FadeIn(dates2))),
            run_time=0.8))
        self.finish()


class S01Prague(BioScene):
    def construct(self):
        self.add_column()
        prague = self.chip_at("Prague", TEAL, CX, 2.2, 34)
        hall = T("the dissection hall", 28, GREY).next_to(prague, DOWN, buff=0.3)
        self.play(FadeIn(prague, shift=UP * 0.1), run_time=0.5)
        self.at("dissection hall")
        self.play(FadeIn(hall, shift=UP * 0.1), run_time=0.4)

        carl = Circle(radius=0.42, color=GREY, fill_color=GREY, fill_opacity=0.25, stroke_width=4)
        gerty = carl.copy()
        carl.move_to([CX - 3.4, -0.6, 0]); gerty.move_to([CX + 3.4, -0.6, 0])
        lc = T("Carl", 26, GREY).next_to(carl, DOWN, buff=0.22)
        lg = T("Gerty", 26, GREY).next_to(gerty, DOWN, buff=0.22)
        gc, gg = VGroup(carl, lc), VGroup(gerty, lg)
        self.at("and recognized")
        self.play(FadeIn(gc, shift=RIGHT * 0.3), FadeIn(gg, shift=LEFT * 0.3), run_time=0.5)
        self.play(gc.animate.shift(RIGHT * 2.3), gg.animate.shift(LEFT * 2.3), run_time=1.5)
        self.at("same kind of person")
        link = Line(carl.get_right(), gerty.get_left(), color=GOLD, stroke_width=5)
        same = T("the same kind of person", 34, GOLD, font=TITLE_FONT).move_to([CX, -2.5, 0])
        self.play(carl.animate.set_color(GOLD).set_fill(GOLD, 0.35), gerty.animate.set_color(GOLD).set_fill(GOLD, 0.35),
                  lc.animate.set_color(GOLD), lg.animate.set_color(GOLD),
                  Create(link), FadeIn(same, shift=UP * 0.1), run_time=0.9)
        self.finish()


class S02NewWorld(BioScene):
    def construct(self):
        self.add_column()
        prague = self.chip_at("Prague", TEAL, -0.9, 2.2, 30)
        married = T("married", 26, GOLD).next_to(prague, DOWN, buff=0.2)
        self.play(FadeIn(prague), FadeIn(married), run_time=0.5)
        self.at("came to the United")
        us = self.chip_at("United States", TEAL, 4.4, 2.2, 30)
        arr = Arrow(prague.get_right() + RIGHT * 0.1, us.get_left() + LEFT * 0.1, buff=0, color=GREY, stroke_width=5,
                    max_tip_length_to_length_ratio=0.2)
        self.play(GrowArrow(arr), FadeIn(us, shift=LEFT * 0.2), run_time=0.8)
        self.at("1922")
        yr = M("1922", 40, YELLOW).move_to([1.7, 2.95, 0])
        self.play(Write(yr), run_time=0.5)

        self.at("ran headlong")
        band = Rectangle(width=8.4, height=0.62, stroke_width=0, fill_color=RED, fill_opacity=0.2).move_to([CX, 0.65, 0])
        rules = T("the rules of the era", 28, RED).move_to(band)
        self.play(FadeIn(band, shift=RIGHT * 0.3), FadeIn(rules), run_time=0.7)

        self.at("A Buffalo Institute")
        dirc = self.chip_at("Buffalo institute director", TEAL, CX, -0.55, 28)
        self.play(FadeIn(dirc, shift=UP * 0.1), run_time=0.5)
        self.at("ordered Gertie")
        order = T("stop publishing with her husband", 30, RED).move_to([CX, -1.9, 0])
        down = Arrow(dirc.get_bottom() + DOWN * 0.05, order.get_top() + UP * 0.12, buff=0, color=RED, stroke_width=4,
                     max_tip_length_to_length_ratio=0.35)
        self.play(GrowArrow(down), FadeIn(order, shift=DOWN * 0.1), run_time=0.7)
        self.at("and she refused")
        strike = Line(order.get_left() + LEFT * 0.1, order.get_right() + RIGHT * 0.1, color=GOLD, stroke_width=6)
        refused = T("She refused.", 38, GOLD, font=TITLE_FONT).move_to([CX, -2.95, 0])
        self.play(Create(strike), run_time=0.4)
        self.play(FadeIn(refused, shift=UP * 0.1), run_time=0.4)

        # clear the stage
        self.at("At Washington University", lead=0.5)
        phaseA = Group(prague, married, arr, us, yr, band, rules, dirc, down, order, strike, refused)
        self.play(FadeOut(phaseA), run_time=0.4)
        wu = self.chip_at("Washington University", TEAL, CX, 2.9, 30)
        self.play(FadeIn(wu, shift=DOWN * 0.1), run_time=0.5)

        # salary bars (the story says a tenth; no amounts)
        x0, full = -0.1, 6.0
        ycarl, ygerty = 1.4, 0.5
        lab_c = T("Carl's salary", 26, GREY).move_to([x0 - 0.2 - 1.05, ycarl, 0])
        lab_g = T("Gerty's salary", 26, GOLD).move_to([x0 - 0.2 - 1.05, ygerty, 0])
        lab_c.align_to([x0 - 0.25, 0, 0], RIGHT); lab_g.align_to([x0 - 0.25, 0, 0], RIGHT)
        bar_c = Rectangle(width=full, height=0.5, stroke_width=0, fill_color=GREY, fill_opacity=0.8)
        bar_c.move_to([x0 + full / 2, ycarl, 0])
        self.at("she was hired")
        self.play(FadeIn(lab_c), GrowFromEdge(bar_c, LEFT), run_time=0.5)
        self.at("a tenth")
        self.play(FadeIn(lab_g), run_time=0.15)
        bar_g = Rectangle(width=full / 10, height=0.5, stroke_width=0, fill_color=GOLD, fill_opacity=0.9)
        bar_g.move_to([x0 + full / 20, ygerty, 0])
        tenth = T("one tenth", 28, RED).next_to(bar_g, RIGHT, buff=0.3)
        self.play(GrowFromEdge(bar_g, LEFT), run_time=0.6)
        self.play(FadeIn(tenth, shift=RIGHT * 0.2), run_time=0.4)

        self.at("for 16 years")
        blocks = VGroup(*[Square(0.28, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9) for _ in range(16)])
        blocks.arrange(RIGHT, buff=0.1).move_to([x0 + 3.05, -0.65, 0])
        yrs = T("16 years", 28, YELLOW).move_to([x0 - 0.25 - 0.95, -0.65, 0])
        yrs.align_to([x0 - 0.25, 0, 0], RIGHT)
        self.play(FadeIn(yrs), LaggedStart(*[FadeIn(b, scale=0.5) for b in blocks], lag_ratio=0.12), run_time=1.0)
        self.at("under nepotism", lead=0.55)
        nep = self.chip_at("under nepotism rules", RED, CX + 0.2, -2.1, 30)
        self.play(FadeIn(nep, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S03Discovery(BioScene):
    def construct(self):
        self.add_column()
        # --- the lab trained five future Nobel laureates
        lab = self.chip_at("the lab Gerty built", GOLD, CX, 2.4, 32)
        self.play(FadeIn(lab, shift=DOWN * 0.1), run_time=0.5)
        self.at("five")
        dots = VGroup()
        for i in range(5):
            d = VGroup(Circle(radius=0.4, color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.22),
                       M(str(i + 1), 26, GOLD))
            d.move_to([CX - 3.0 + 1.5 * i, 0.5, 0])
            dots.add(d)
        self.play(LaggedStart(*[FadeIn(d, scale=0.6) for d in dots], lag_ratio=0.5), run_time=1.1)
        self.at("laureates")
        lbl = T("five future Nobel laureates", 32, GOLD, font=TITLE_FONT).move_to([CX, -0.8, 0])
        self.play(FadeIn(lbl, shift=UP * 0.1), run_time=0.5)

        # --- clear; the discarded fraction
        self.at("working through", lead=0.4)
        self.play(FadeOut(Group(lab, dots, lbl)), run_time=0.35)
        tx, ty, tw, th = -0.2, 0.2, 1.4, 3.4
        tube = RoundedRectangle(corner_radius=0.25, width=tw, height=th, stroke_color=GREY, stroke_width=4).move_to([tx, ty, 0])
        pellet = Rectangle(width=tw - 0.12, height=0.8, stroke_width=0, fill_color=BLUE, fill_opacity=0.75)
        pellet.move_to([tx, ty - th / 2 + 0.4 + 0.06, 0])
        sup = Rectangle(width=tw - 0.12, height=2.45, stroke_width=0, fill_color=AMBER, fill_opacity=0.4)
        sup.move_to([tx, pellet.get_top()[1] + 1.225, 0])
        self.play(Create(tube), GrowFromEdge(pellet, DOWN), GrowFromEdge(sup, DOWN), run_time=0.7)
        lab_frac = T("a fraction", 28, AMBER).move_to([2.7, 1.1, 0])
        ptr1 = Arrow(lab_frac.get_left() + LEFT * 0.1, [tx + tw / 2 + 0.1, 1.1, 0], buff=0, color=AMBER, stroke_width=3,
                     max_tip_length_to_length_ratio=0.3)
        self.play(FadeIn(lab_frac), GrowArrow(ptr1), run_time=0.4)
        self.at("everyone else threw")
        bin_ = self.chip_at("thrown away", RED, 3.6, 2.75, 28)
        toss = CurvedArrow([tx + 0.2, ty + th / 2 + 0.05, 0], bin_.get_left() + LEFT * 0.1, angle=-TAU / 6, color=RED, stroke_width=4)
        self.play(Create(toss), FadeIn(bin_, shift=LEFT * 0.2), run_time=0.9)

        self.at("The supernatant")
        sup_lbl = T("supernatant", 28, AMBER).move_to(lab_frac)
        sup_lbl.align_to(lab_frac, LEFT)
        self.play(FadeOut(Group(toss, bin_)), ReplacementTransform(lab_frac, sup_lbl),
                  sup.animate.set_fill(AMBER, 0.6), run_time=0.7)
        self.at("left from recrystallizing")
        lab_ph = VGroup(T("recrystallizing", 26, BLUE), T("phosphorylase", 26, BLUE)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        lab_ph.move_to([2.7, -1.15, 0]).align_to([1.6, 0, 0], LEFT)
        ptr2 = Arrow([1.5, pellet.get_center()[1], 0], [tx + tw / 2 + 0.1, pellet.get_center()[1], 0], buff=0, color=BLUE,
                     stroke_width=3, max_tip_length_to_length_ratio=0.3)
        self.play(FadeIn(lab_ph), GrowArrow(ptr2), Indicate(pellet, color=BLUE, scale_factor=1.05), run_time=0.9)

        self.at("They found the debranching")
        deb = self.chip_at("debranching enzyme", BLUE, 3.7, 0.15, 30)
        a3 = Arrow([tx + tw / 2 + 0.15, 0.15, 0], deb.get_left() + LEFT * 0.08, buff=0, color=GOLD, stroke_width=5,
                   max_tip_length_to_length_ratio=0.3)
        self.play(GrowArrow(a3), FadeIn(deb, scale=0.9), run_time=0.8)
        self.play(Indicate(deb, color=GOLD, scale_factor=1.06), run_time=0.7)

        # --- the chromatography spot
        self.at("and Gertie understood", lead=0.5)
        self.play(FadeOut(Group(tube, pellet, sup, sup_lbl, ptr1, lab_ph, ptr2, deb, a3)), run_time=0.35)
        strip = Rectangle(width=1.3, height=3.0, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12)
        strip.move_to([-0.8, 1.0, 0])
        spot = Circle(radius=0.2, color=GREEN, stroke_width=0, fill_color=GREEN, fill_opacity=0.9).move_to([-0.8, 0.45, 0])
        self.play(FadeIn(strip), run_time=0.4)
        self.play(GrowFromCenter(spot), run_time=0.4)
        cs = T("chromatography spot", 28, GREY).move_to([2.7, 0.45, 0])
        ptr3 = Arrow(cs.get_left() + LEFT * 0.1, spot.get_right() + RIGHT * 0.1, buff=0, color=GREY, stroke_width=3,
                     max_tip_length_to_length_ratio=0.3)
        self.play(FadeIn(cs), GrowArrow(ptr3), run_time=0.5)
        self.at("instantly")
        fg = T("free glucose", 30, GREEN).move_to([2.3, 0.45, 0])
        fg.align_to(cs, LEFT)
        ring = Circle(radius=0.36, color=GOLD, stroke_width=4).move_to(spot)
        self.play(ReplacementTransform(cs, fg), Create(ring), run_time=0.7)

        # --- ran down the hall, shouting
        self.at("ran down")
        hall_y = -2.75
        hall = Line([-2.0, hall_y, 0], [6.1, hall_y, 0], color=GREY, stroke_width=3)
        runner = VGroup(Dot(radius=0.2, color=GOLD), T("Gerty", 24, GOLD).shift(UP * 0.5)).move_to([-2.0, hall_y + 0.3, 0])
        hall_lbl = T("down the hall", 24, GREY).move_to([CX, hall_y - 0.4, 0])
        self.play(Create(hall), FadeIn(hall_lbl), FadeIn(runner), run_time=0.4)
        self.play(runner.animate.move_to([5.8, hall_y + 0.3, 0]), run_time=1.5, rate_func=smooth)
        self.at("it's free glucose")
        shout = T("“It’s free glucose, it’s free glucose!”", 36, GREEN, font=TITLE_FONT).move_to([CX, -1.25, 0])
        fit(shout, max_w=8.6)
        self.play(Write(shout), run_time=2.2)
        self.finish()


class S04Disease(BioScene):
    def construct(self):
        self.add_column()
        self.at("matching the wrong")
        gly = self.chip_at("wrong-shaped glycogen", GREEN, CX, 2.8, 28)
        self.play(FadeIn(gly, shift=DOWN * 0.1), run_time=0.6)
        self.at("in sick children")
        kids = T("in sick children", 26, GREY).move_to([CX, 2.05, 0])
        self.play(FadeIn(kids, shift=UP * 0.1), run_time=0.4)

        self.at("to a specific missing")
        arr = Arrow([CX, 1.75, 0], [CX, 1.0, 0], buff=0, color=GREY, stroke_width=5, max_tip_length_to_length_ratio=0.35)
        matched = T("matched to", 24, GREY).next_to(arr, RIGHT, buff=0.25)
        enz = chip("a specific missing enzyme", BLUE, 28).move_to([CX, 0.45, 0])
        box = enz[0]
        dashed = DashedVMobject(box, num_dashes=44, dashed_ratio=0.55).set_color(BLUE)
        enz_f = VGroup(dashed, enz[1])
        self.play(GrowArrow(arr), FadeIn(matched), run_time=0.5)
        self.play(FadeIn(enz_f, shift=UP * 0.1), run_time=0.6)

        self.at("the first proof")
        gold = T("the first proof", 32, GOLD, font=TITLE_FONT).move_to([CX, -0.7, 0])
        gl = Line([CX - 2.6, -1.1, 0], [CX + 2.6, -1.1, 0], color=GOLD, stroke_width=3)
        self.play(FadeIn(gold, shift=UP * 0.1), Create(gl), run_time=0.6)
        self.at("one broken enzyme")
        one = chip("one broken enzyme", BLUE, 28).move_to([CX - 2.5, -2.15, 0])
        one_f = VGroup(DashedVMobject(one[0], num_dashes=40, dashed_ratio=0.55).set_color(BLUE), one[1])
        self.play(FadeIn(one_f, shift=UP * 0.1), run_time=0.5)
        self.at("can cause")
        dis = chip("inherited disease", RED, 28).move_to([CX + 2.2, -2.15, 0])
        a2 = Arrow(one.get_right() + RIGHT * 0.1, dis.get_left() + LEFT * 0.1, buff=0, color=GOLD, stroke_width=5,
                   max_tip_length_to_length_ratio=0.35)
        self.play(GrowArrow(a2), run_time=0.4)
        self.at("inherited disease")
        self.play(FadeIn(dis, shift=LEFT * 0.2), run_time=0.5)
        self.finish()


class S05Nobel(BioScene):
    def construct(self):
        self.add_column()
        self.at("the Nobel")
        medal = VGroup(Circle(radius=0.68, color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.2),
                       T("Nobel", 24, GOLD, weight=BOLD)).move_to([CX - 1.5, 2.55, 0])
        self.play(GrowFromCenter(medal), run_time=0.6)
        self.at("1947")
        yr = M("1947", 60, YELLOW).move_to([CX + 1.2, 2.55, 0])
        self.play(Write(yr), run_time=0.6)

        self.at("Carl said")
        said = T("Carl, at the banquet", 28, GREY).move_to([CX, 1.3, 0])
        self.play(FadeIn(said, shift=UP * 0.1), run_time=0.5)
        self.at("including his wife")
        inc = T("including his wife", 32, TEXT, font=TITLE_FONT).move_to([CX, 0.55, 0])
        self.play(FadeIn(inc, shift=UP * 0.1), run_time=0.5)
        self.at("a source of deep")
        q1 = T("“a source of deep", 38, GOLD, font=TITLE_FONT)
        q2 = T("satisfaction to me”", 38, GOLD, font=TITLE_FONT)
        q = VGroup(q1, q2).arrange(DOWN, buff=0.18).move_to([CX, -0.65, 0])
        self.play(Write(q, run_time=2.4))

        self.at("He was not being gallant")
        gal = T("gallant", 40, GREY, font=TITLE_FONT).move_to([CX - 1.9, -2.6, 0])
        self.play(FadeIn(gal, shift=UP * 0.1), run_time=0.4)
        self.at("being gallant")
        cross = Line(gal.get_left() + LEFT * 0.1, gal.get_right() + RIGHT * 0.1, color=RED, stroke_width=5)
        self.play(Create(cross), run_time=0.4)
        self.at("he was being accurate")
        acc = T("accurate", 40, GOLD, font=TITLE_FONT).move_to([CX + 1.9, -2.6, 0])
        ul = Line(acc.get_corner(DL) + DOWN * 0.08, acc.get_corner(DR) + DOWN * 0.08, color=GOLD, stroke_width=5)
        self.play(FadeIn(acc, shift=UP * 0.1), Create(ul), run_time=0.7)

        # --- the same year: a timeline
        self.at("The same year", lead=0.45)
        self.play(FadeOut(Group(medal, yr, said, inc, q, gal, cross, acc, ul)), run_time=0.4)
        ty = 1.0
        x22, x47 = 0.0, 4.2
        line = Line([x22 - 0.9, ty, 0], [x47 + 1.5, ty, 0], color=GREY, stroke_width=4)
        t22 = Line([x22, ty - 0.18, 0], [x22, ty + 0.18, 0], color=YELLOW, stroke_width=5)
        t47 = Line([x47, ty - 0.18, 0], [x47, ty + 0.18, 0], color=YELLOW, stroke_width=5)
        y22 = M("1922", 38, YELLOW).move_to([x22, ty + 0.65, 0])
        y47 = M("1947", 38, YELLOW).move_to([x47, ty + 0.65, 0])
        us = T("came to the United States", 24, GREY).move_to([x22, ty - 0.6, 0])
        nob = T("Nobel", 30, GOLD).move_to([x47 + 0.0, ty + 1.35, 0])
        self.at("The same year")
        self.play(Create(line), FadeIn(VGroup(t22, y22, us)), run_time=0.5)
        self.play(FadeIn(VGroup(t47, y47)), FadeIn(nob), run_time=0.4)
        self.at("Washington University", nth=0)
        wu = self.chip_at("Washington University", TEAL, 3.95, -0.7, 26)
        drop = Line([x47, ty - 0.2, 0], [x47, wu.get_top()[1] + 0.05, 0], color=GREY, stroke_width=3)
        self.play(Create(drop), FadeIn(wu, shift=UP * 0.1), run_time=0.6)
        self.at("made Gertie a full")
        prof = self.chip_at("Gerty: full professor", GOLD, 3.95, -1.95, 28)
        self.play(FadeIn(prof, shift=UP * 0.1), run_time=0.6)
        self.play(Indicate(prof, color=GOLD, scale_factor=1.05), run_time=0.7)
        self.finish()


class S06Quote(BioScene):
    def construct(self):
        self.add_column()
        mark = T("“", 120, GOLD, font=TITLE_FONT).move_to([-1.9, 2.0, 0])
        lines = [T("That the award should have included", 36, TEXT, font=TITLE_FONT),
                 T("my wife as well has been a source", 36, TEXT, font=TITLE_FONT),
                 T("of deep satisfaction to me”", 36, TEXT, font=TITLE_FONT)]
        qg = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        fit(qg, max_w=8.6)
        qg.move_to([CX + 0.1, 0.5, 0])
        mark.scale(0.7).next_to(lines[0], LEFT, buff=0.12).align_to(lines[0], UP).shift(UP * 0.12)
        att = T("Carl Cori, at the Nobel banquet, 1947", 28, GOLD).next_to(qg, DOWN, buff=0.6).align_to(qg, RIGHT)
        self.play(FadeIn(mark, shift=DOWN * 0.1), run_time=0.6)
        t = 0.8
        for ln in lines:
            self.play(FadeIn(ln, shift=UP * 0.1), run_time=0.9)
            self.wait(0.5)
        self.play(FadeIn(att, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07End(BioScene):
    LINE = "Traced the Cori cycle; first tied one missing enzyme to inherited disease."

    def construct(self):
        img, border = portrait(height=2.3, center=(0, 2.0))
        cap = T(CAPTION, 22, GREY).move_to([0, 2.0 - 1.15 - 0.3, 0])
        line = T("Traced the Cori cycle; first tied one missing", 38, font=TITLE_FONT)
        line2 = T("enzyme to inherited disease.", 38, font=TITLE_FONT)
        lg = VGroup(line, line2).arrange(DOWN, buff=0.2).move_to([0, -0.55, 0])
        fit(lg, max_w=11.5)
        sub = T("biochemistrypedia.com", 24, TEAL).move_to([0, -1.85, 0])
        src = T("Source: The Molecule Hunters (v10) · Carl and Gerty Cori profile", 22, GREY).move_to([0, -2.6, 0])
        self.play(FadeIn(img), FadeIn(border), FadeIn(cap), run_time=0.5)
        self.play(FadeIn(lg, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(sub), FadeIn(src), run_time=0.4)
        self.finish()
