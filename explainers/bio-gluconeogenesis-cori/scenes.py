"""Carl Cori & Gerty Cori: scientist profile video (Biochemistrypedia, gluconeogenesis lesson)

The portrait (public/scientists/cori.png, an AI-generated engraving-style illustration from
The Molecule Hunters) is the anchor: the title scene pushes in on it, then it stays as a framed
inset on the left while the right side animates the story's beats as the narrator reaches them.
Every cue is a self.at("spoken words") lookup in audio/words.json (word timestamps of the real audio).
Nothing on screen adds a fact that is not in the lesson entry (name, dates, contribution, story, quotes).
Story narrated verbatim from the gluconeogenesis entry, minus the one sentence about the lab's five laureates.

COLOR MAP (one color per concept, whole video)
  GOLD   = the Coris, the portrait frame, recognition (Cori cycle title, "she refused", full professor)
  YELLOW = years / dates, the sixteen years, the decade
  TEAL   = places and institutions (Prague, United States, Buffalo, Washington University)
  RED    = obstacles and harm (the director's order, the salary gap, nepotism rules, disease)
  BLUE   = enzymes (debranching enzyme, glucose-6-phosphatase, the missing enzymes)
  GREEN  = glucose and glycogen ("free glucose", wrong-shaped glycogen)
  PURPLE = lactate
  ORANGE = energy spent by the liver
  AMBER  = the discarded fraction
  GREY   = structure, labels, organs, Carl's salary bar
"""
import os
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

config.disable_caching = True

AMBER = "#E0A458"
PURPLE = "#B58CE0"
ORANGE = "#E8844A"
CX = 1.9            # centre of the content area to the right of the portrait column
PORT_X = -4.8      # portrait column centre
PORT_H = 3.5
PORT_Y = 1.25
CROP_AR = 800 / 760.0   # cori_crop.png: full engraving, both faces complete (cropped from public/scientists/cori.png)
IMG = Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent / "cori_crop.png"
NAME = "Carl Cori & Gerty Cori"
DATES = "Carl 1896–1984 · Gerty 1896–1957"
CAPTION = "illustration · AI-generated"
DIM = 0.62


def portrait(height=PORT_H, center=(PORT_X, PORT_Y)):
    img = ImageMobject(str(IMG))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["cubic"])
    img.set_height(height)
    img.move_to([center[0], center[1], 0])
    img.set_z_index(0)
    border = Rectangle(width=img.width, height=img.height, stroke_color=GOLD, stroke_width=3, fill_opacity=0)
    border.move_to(img).set_z_index(3)
    return img, border


def dimmers(focus="both", height=PORT_H, center=(PORT_X, PORT_Y)):
    """Two half-frame veils over the portrait: left half = Carl, right half = Gerty."""
    w = height * CROP_AR
    mk = lambda dx, op: Rectangle(width=w / 2, height=height, stroke_width=0, fill_color=BG,
                                  fill_opacity=op).move_to([center[0] + dx, center[1], 0]).set_z_index(2)
    return (mk(-w / 4, DIM if focus == "right" else 0), mk(w / 4, DIM if focus == "left" else 0))


def column_labels(focus="both"):
    """Caption plus a name and years under each face (Carl left, Gerty right)."""
    w = PORT_H * CROP_AR
    y = PORT_Y - PORT_H / 2
    cap = T(CAPTION, 22, GREY).move_to([PORT_X, y - 0.32, 0])
    nl = VGroup(T("Carl Cori", 24, TEXT, font=TITLE_FONT), T("1896–1984", 22, GOLD)).arrange(DOWN, buff=0.1)
    nr = VGroup(T("Gerty Cori", 24, TEXT, font=TITLE_FONT), T("1896–1957", 22, GOLD)).arrange(DOWN, buff=0.1)
    nl.move_to([PORT_X - w / 4, y - 1.12, 0]); nr.move_to([PORT_X + w / 4, y - 1.12, 0])
    nl.set_opacity(0.4 if focus == "right" else 1)
    nr.set_opacity(0.4 if focus == "left" else 1)
    return cap, nl, nr


def focus_anims(plate, which):
    """Animations that move the highlight to 'left' (Carl), 'right' (Gerty) or 'both'."""
    dl, dr, nl, nr = plate
    return [dl.animate.set_fill(BG, opacity=DIM if which == "right" else 0),
            dr.animate.set_fill(BG, opacity=DIM if which == "left" else 0),
            nl.animate.set_opacity(0.4 if which == "right" else 1),
            nr.animate.set_opacity(0.4 if which == "left" else 1)]


def dashed_chip(text, color, size=28):
    """A chip with a dashed outline: 'something missing'."""
    c = chip(text, color, size)
    return VGroup(DashedVMobject(c[0], num_dashes=44, dashed_ratio=0.55).set_color(color), c[1])


class BioScene(SpokenScene):
    def add_column(self, focus="both"):
        img, border = portrait()
        cap, nl, nr = column_labels(focus)
        dl, dr = dimmers(focus)
        self.add(img, border, dl, dr, cap, nl, nr)
        self.plate = (dl, dr, nl, nr)

    def focus(self, which):
        return focus_anims(self.plate, which)

    def chip_at(self, text, color, x, y, size=28, **kw):
        c = chip(text, color, size, **kw)
        c.move_to([x, y, 0])
        return c


class S00Title(BioScene):
    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA  ·  SCIENTIST PROFILE", 22, TEAL, weight=BOLD).move_to([0, 3.4, 0])
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
        self.play(img.animate.scale(1.05), border.animate.scale(1.05),
                  Write(name, run_time=1.0), run_time=1.5, rate_func=linear)
        self.play(GrowFromCenter(rule), FadeIn(dates), run_time=0.35)
        cap2, nl, nr = column_labels()
        self.play(AnimationGroup(
            img.animate.scale(1 / (k * 1.05)).move_to([PORT_X, PORT_Y, 0]),
            border.animate.scale(1 / (k * 1.05)).move_to([PORT_X, PORT_Y, 0]),
            cap.animate.move_to(cap2),
            Succession(AnimationGroup(FadeOut(name), FadeOut(dates), FadeOut(rule), FadeOut(brand)),
                       AnimationGroup(FadeIn(nl), FadeIn(nr))),
            run_time=0.8))
        self.finish()


class S01Origins(BioScene):
    def construct(self):
        self.add_column()
        # --- Prague: they recognize each other
        prague = self.chip_at("Prague", TEAL, CX, 2.2, 34)
        hall = T("the dissection hall", 28, GREY).next_to(prague, DOWN, buff=0.3)
        carl = Circle(radius=0.42, color=GREY, fill_color=GREY, fill_opacity=0.25, stroke_width=4)
        gerty = carl.copy()
        carl.move_to([CX - 3.4, -0.6, 0]); gerty.move_to([CX + 3.4, -0.6, 0])
        lc = T("Carl", 26, GREY).next_to(carl, DOWN, buff=0.22)
        lg = T("Gerty", 26, GREY).next_to(gerty, DOWN, buff=0.22)
        gc, gg = VGroup(carl, lc), VGroup(gerty, lg)
        self.play(FadeIn(prague, shift=UP * 0.1), FadeIn(gc, shift=RIGHT * 0.3), FadeIn(gg, shift=LEFT * 0.3),
                  run_time=0.5)
        self.at("dissection hall")
        self.play(FadeIn(hall, shift=UP * 0.1), gc.animate.shift(RIGHT * 1.0), gg.animate.shift(LEFT * 1.0),
                  run_time=1.5, rate_func=linear)
        self.at("recognized")
        self.play(gc.animate.shift(RIGHT * 1.3), gg.animate.shift(LEFT * 1.3), run_time=1.5, rate_func=linear)
        self.at("same kind of person")
        link = Line(carl.get_right(), gerty.get_left(), color=GOLD, stroke_width=5)
        same = T("the same kind of person", 34, GOLD, font=TITLE_FONT).move_to([CX, -2.5, 0])
        self.play(carl.animate.set_color(GOLD).set_fill(GOLD, 0.35), gerty.animate.set_color(GOLD).set_fill(GOLD, 0.35),
                  lc.animate.set_color(GOLD), lg.animate.set_color(GOLD),
                  Create(link), FadeIn(same, shift=UP * 0.1), run_time=0.8)

        # --- they married, came to the United States in 1922
        self.at("They married", lead=0.35)
        self.play(FadeOut(Group(gc, gg, link, same, hall)), prague.animate.scale(30 / 34).move_to([-0.9, 2.2, 0]),
                  run_time=0.4)
        married = T("married", 26, GOLD).next_to(prague, DOWN, buff=0.2)
        self.play(FadeIn(married), run_time=0.3)
        self.at("came to the United")
        us = self.chip_at("United States", TEAL, 4.4, 2.2, 30)
        arr = Arrow(prague.get_right() + RIGHT * 0.1, us.get_left() + LEFT * 0.1, buff=0, color=GREY, stroke_width=5,
                    max_tip_length_to_length_ratio=0.2)
        self.play(GrowArrow(arr), FadeIn(us, shift=LEFT * 0.2), run_time=0.7)
        self.at("1922")
        yr = M("1922", 40, YELLOW).move_to([1.7, 2.95, 0])
        self.play(Write(yr), run_time=0.5)

        # --- the rules of the era, the Buffalo director
        self.at("ran into")
        band = Rectangle(width=8.4, height=0.62, stroke_width=0, fill_color=RED, fill_opacity=0.2).move_to([CX, 0.65, 0])
        rules = T("the rules of the era", 28, RED).move_to(band)
        self.play(FadeIn(band, shift=RIGHT * 0.3), FadeIn(rules), run_time=0.7)
        self.at("head on")
        self.play(Indicate(band, color=RED, scale_factor=1.05), Indicate(rules, color=RED, scale_factor=1.15),
                  run_time=0.9)

        self.at("Buffalo")
        dirc = self.chip_at("Buffalo institute director", TEAL, CX, -0.55, 28)
        self.play(FadeIn(dirc, shift=UP * 0.1), run_time=0.5)
        self.at("ordered Gertie")
        order = T("stop publishing with her husband", 30, RED).move_to([CX, -1.9, 0])
        down = Arrow(dirc.get_bottom() + DOWN * 0.05, order.get_top() + UP * 0.12, buff=0, color=RED, stroke_width=4,
                     max_tip_length_to_length_ratio=0.35)
        self.play(GrowArrow(down), *self.focus("right"), run_time=0.5)
        self.at("stop publishing")
        self.play(Write(order), run_time=1.6)
        self.at("and she refused")
        strike = Line(order.get_left() + LEFT * 0.1, order.get_right() + RIGHT * 0.1, color=GOLD, stroke_width=6)
        refused = T("She refused.", 38, GOLD, font=TITLE_FONT).move_to([CX, -2.95, 0])
        self.play(Create(strike), run_time=0.4)
        self.play(FadeIn(refused, shift=UP * 0.1), run_time=0.4)

        # --- Washington University: a tenth of Carl's salary
        self.at("Washington University", lead=0.4)
        phaseA = Group(prague, married, arr, us, yr, band, rules, dirc, down, order, strike, refused)
        self.play(FadeOut(phaseA), run_time=0.4)
        wu = self.chip_at("Washington University", TEAL, CX, 2.9, 30)
        self.play(FadeIn(wu, shift=DOWN * 0.1), run_time=0.5)

        x0, full = -0.1, 6.0
        ycarl, ygerty = 1.4, 0.5
        lab_c = T("Carl's salary", 26, GREY).move_to([x0 - 1.25, ycarl, 0])
        lab_g = T("Gerty's salary", 26, GOLD).move_to([x0 - 1.25, ygerty, 0])
        lab_c.align_to([x0 - 0.25, 0, 0], RIGHT); lab_g.align_to([x0 - 0.25, 0, 0], RIGHT)
        bar_c = Rectangle(width=full, height=0.5, stroke_width=0, fill_color=GREY, fill_opacity=0.8)
        bar_c.move_to([x0 + full / 2, ycarl, 0])
        self.at("hired")
        self.play(FadeIn(lab_c), GrowFromEdge(bar_c, LEFT), run_time=0.5)
        self.at("a tenth")
        self.play(FadeIn(lab_g), run_time=0.15)
        bar_g = Rectangle(width=full / 10, height=0.5, stroke_width=0, fill_color=GOLD, fill_opacity=0.9)
        bar_g.move_to([x0 + full / 20, ygerty, 0])
        tenth = T("one tenth", 28, RED).next_to(bar_g, RIGHT, buff=0.3)
        self.play(GrowFromEdge(bar_g, LEFT), run_time=0.5)
        self.play(FadeIn(tenth, shift=RIGHT * 0.2), run_time=0.4)

        self.at("16 years")
        blocks = VGroup(*[Square(0.28, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9) for _ in range(16)])
        blocks.arrange(RIGHT, buff=0.1).move_to([x0 + 3.05, -0.65, 0])
        yrs = T("16 years", 28, YELLOW).move_to([x0 - 1.2, -0.65, 0])
        yrs.align_to([x0 - 0.25, 0, 0], RIGHT)
        self.play(FadeIn(yrs), LaggedStart(*[FadeIn(b, scale=0.5) for b in blocks], lag_ratio=0.1), run_time=0.9)
        self.at("under nepotism", lead=0.55)
        nep = self.chip_at("under nepotism rules", RED, CX + 0.2, -2.1, 30)
        self.play(FadeIn(nep, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S02Cycle(BioScene):
    def organ(self, name, cx):
        box = RoundedRectangle(corner_radius=0.2, width=3.2, height=3.2, stroke_color=GREY, stroke_width=3,
                               fill_color=GREY, fill_opacity=0.07).move_to([cx, 0.15, 0])
        lab = T(name, 26, GREY, weight=BOLD).move_to([cx, 1.45, 0])
        return VGroup(box, lab)

    def construct(self):
        self.add_column()
        # --- the work on the side of tumor metabolism
        cycle = self.chip_at("The Cori cycle", GOLD, CX, 2.9, 34)
        self.play(FadeIn(cycle, shift=DOWN * 0.1), run_time=0.6)
        self.at("came out of")
        side = T("grew out of work done on the side of", 26, GREY).move_to([CX, 1.85, 0])
        self.play(Write(side), run_time=1.4)
        self.at("tumor metabolism")
        tumor = self.chip_at("tumor metabolism", GREY, CX, 0.8, 32)
        self.play(FadeIn(tumor, shift=UP * 0.1), run_time=0.5)
        self.at("were paid")
        paid = T("the work they were paid to study", 26, GREY).move_to([CX, -0.3, 0])
        self.play(FadeIn(paid, shift=UP * 0.1), run_time=0.5)

        # --- muscle -> lactate -> blood -> liver -> glucose
        self.at("muscle breaks", lead=0.3)
        self.play(FadeOut(Group(cycle, side, tumor, paid)), run_time=0.35)
        mx, lx = -0.1, 4.3
        muscle = self.organ("muscle", mx)
        liver = self.organ("liver", lx)
        self.play(GrowFromCenter(muscle), run_time=0.5)
        self.at("glucose to")
        glu_m = self.chip_at("glucose", GREEN, mx, 0.6, 26)
        self.play(FadeIn(glu_m, shift=DOWN * 0.1), run_time=0.4)
        self.at("lactate")
        a_m = Arrow([mx, 0.15, 0], [mx, -0.5, 0], buff=0, color=GREY, stroke_width=4, max_tip_length_to_length_ratio=0.35)
        lac_m = self.chip_at("lactate", PURPLE, mx, -0.95, 26)
        self.play(GrowArrow(a_m), FadeIn(lac_m, shift=DOWN * 0.1), run_time=0.6)

        self.at("the blood carries")
        blood = Arrow([mx + 1.65, -0.95, 0], [lx - 1.65, -0.95, 0], buff=0, color=GREY, stroke_width=4,
                      max_tip_length_to_length_ratio=0.3)
        blood_l = T("blood", 24, GREY).move_to([(mx + lx) / 2, -0.5, 0])
        self.play(GrowFromCenter(liver), GrowArrow(blood), FadeIn(blood_l), run_time=0.6)
        self.at("carries the lactate")
        lac_t = lac_m.copy()
        self.play(lac_t.animate.move_to([lx, -0.95, 0]), run_time=0.9)

        self.at("the liver spends")
        a_l = Arrow([lx, -0.5, 0], [lx, 0.15, 0], buff=0, color=GREY, stroke_width=4, max_tip_length_to_length_ratio=0.35)
        en = VGroup(T("spends", 24, ORANGE), T("energy", 24, ORANGE)).arrange(DOWN, buff=0.04).move_to([lx + 0.85, -0.17, 0])
        self.play(GrowArrow(a_l), FadeIn(en, shift=LEFT * 0.1), run_time=0.6)
        self.at("rebuild glucose", lead=0.35)
        glu_l = self.chip_at("glucose", GREEN, lx, 0.6, 26)
        self.play(FadeIn(glu_l, shift=UP * 0.1), run_time=0.5)

        # the loop closes: glucose goes round again
        ytop = 2.55
        p = [[lx, 1.75, 0], [lx, ytop, 0], [mx, ytop, 0], [mx, 1.75, 0]]
        segs = [Line(p[0], p[1], color=GREEN, stroke_width=5), Line(p[1], p[2], color=GREEN, stroke_width=5),
                Arrow(p[2], p[3], buff=0, color=GREEN, stroke_width=5, max_tip_length_to_length_ratio=0.2)]
        loop_l = T("glucose", 26, GREEN).move_to([(mx + lx) / 2, ytop + 0.4, 0])
        self.play(Succession(*[Create(s) for s in segs]), FadeIn(loop_l), run_time=0.9)
        self.finish()


class S03Discovery(BioScene):
    def construct(self):
        self.add_column("right")
        # --- a fraction everyone else discarded
        tx, ty, tw, th = -0.2, 0.2, 1.4, 3.4
        tube = RoundedRectangle(corner_radius=0.25, width=tw, height=th, stroke_color=GREY, stroke_width=4).move_to([tx, ty, 0])
        frac = Rectangle(width=tw - 0.12, height=2.6, stroke_width=0, fill_color=AMBER, fill_opacity=0.5)
        frac.move_to([tx, ty - th / 2 + 1.3 + 0.06, 0])
        self.play(Create(tube), GrowFromEdge(frac, DOWN), run_time=0.6)
        self.at("fraction")
        lab_frac = T("a fraction", 28, AMBER).move_to([2.7, 1.1, 0])
        ptr1 = Arrow(lab_frac.get_left() + LEFT * 0.1, [tx + tw / 2 + 0.1, 1.1, 0], buff=0, color=AMBER, stroke_width=3,
                     max_tip_length_to_length_ratio=0.3)
        self.play(FadeIn(lab_frac), GrowArrow(ptr1), run_time=0.4)
        self.at("discarded")
        bin_ = self.chip_at("thrown away", RED, 3.6, 2.75, 28)
        toss = CurvedArrow([tx + 0.2, ty + th / 2 + 0.05, 0], bin_.get_left() + LEFT * 0.1, angle=-TAU / 6, color=RED, stroke_width=4)
        self.play(Create(toss), FadeIn(bin_, shift=LEFT * 0.2), run_time=0.9)

        # --- but they chased it and found the debranching enzyme
        self.at("they found")
        self.play(FadeOut(Group(toss, bin_)), Indicate(frac, color=GOLD, scale_factor=1.04), *self.focus("both"),
                  run_time=0.6)
        self.at("glycogen debranching")
        deb = self.chip_at("glycogen debranching\nenzyme", BLUE, 3.9, -0.8, 28)
        a3 = Arrow([tx + tw / 2 + 0.15, -0.8, 0], deb.get_left() + LEFT * 0.08, buff=0, color=GOLD, stroke_width=5,
                   max_tip_length_to_length_ratio=0.3)
        self.play(GrowArrow(a3), FadeIn(deb, scale=0.9), run_time=0.7)
        self.play(Indicate(deb, color=GOLD, scale_factor=1.05), run_time=0.6)

        # --- Gerty reads the chromatography spot
        self.at("Gertie read", lead=0.5)
        self.play(FadeOut(Group(tube, frac, lab_frac, ptr1, deb, a3)), *self.focus("right"), run_time=0.35)
        strip = Rectangle(width=1.3, height=2.4, stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.12)
        strip.move_to([-0.8, 1.5, 0])
        spot = Circle(radius=0.2, color=GREEN, stroke_width=0, fill_color=GREEN, fill_opacity=0.9).move_to([-0.8, 1.0, 0])
        self.play(FadeIn(strip), run_time=0.35)
        self.play(GrowFromCenter(spot), run_time=0.35)
        self.at("chromatography")
        cs = T("chromatography spot", 28, GREY).move_to([2.7, 1.0, 0])
        ptr3 = Arrow(cs.get_left() + LEFT * 0.1, spot.get_right() + RIGHT * 0.1, buff=0, color=GREY, stroke_width=3,
                     max_tip_length_to_length_ratio=0.3)
        self.play(FadeIn(cs), GrowArrow(ptr3), run_time=0.5)
        self.at("instantly")
        fg = T("free glucose", 30, GREEN).move_to([2.3, 1.0, 0])
        fg.align_to(cs, LEFT)
        ring = Circle(radius=0.36, color=GOLD, stroke_width=4).move_to(spot)
        self.play(ReplacementTransform(cs, fg), Create(ring), run_time=0.6)

        # --- ran down the hall, shouting
        self.at("ran down")
        hall_y = -2.75
        hall = Line([-2.0, hall_y, 0], [6.1, hall_y, 0], color=GREY, stroke_width=3)
        runner = VGroup(Dot(radius=0.2, color=GOLD), T("Gerty", 24, GOLD).shift(UP * 0.5)).move_to([-2.0, hall_y + 0.3, 0])
        hall_lbl = T("down the hall", 24, GREY).move_to([CX, hall_y - 0.4, 0])
        self.play(Create(hall), FadeIn(hall_lbl), FadeIn(runner), run_time=0.3)
        self.play(runner.animate.move_to([5.8, hall_y + 0.3, 0]), run_time=1.3, rate_func=smooth)
        self.at("It's free glucose")
        s1 = T("“It’s free glucose,", 38, GREEN, font=TITLE_FONT)
        s2 = T("it’s free glucose!”", 38, GREEN, font=TITLE_FONT)
        shout = VGroup(s1, s2).arrange(DOWN, buff=0.2).move_to([CX, -0.75, 0])
        self.play(Write(s1), run_time=1.0)
        self.at("it's free glucose", nth=1)
        self.play(Write(s2), run_time=1.1)

        # --- the same free glucose that glucose-6-phosphatase releases to the blood
        self.at("The same free glucose", lead=0.4)
        self.play(FadeOut(Group(strip, spot, fg, ptr3, ring, hall, hall_lbl, runner, shout)), run_time=0.4)
        gl = self.chip_at("free glucose", GREEN, CX, 0.2, 32)
        self.play(FadeIn(gl, scale=0.9), run_time=0.5)
        self.at("this chapter's last enzyme")
        last = T("this chapter's last enzyme", 28, GREY).move_to([CX, 2.8, 0])
        self.play(Write(last), run_time=1.3)
        self.at("phosphatase")
        enz = self.chip_at("glucose-6-phosphatase", BLUE, CX, 1.7, 30)
        self.play(FadeIn(enz, shift=DOWN * 0.1), run_time=0.5)
        self.at("releases")
        a_e = Arrow(enz.get_bottom() + DOWN * 0.05, gl.get_top() + UP * 0.05, buff=0, color=BLUE, stroke_width=5,
                    max_tip_length_to_length_ratio=0.35)
        blood = self.chip_at("the blood", GREY, CX, -1.8, 30)
        a_b = Arrow(gl.get_bottom() + DOWN * 0.05, blood.get_top() + UP * 0.05, buff=0, color=GREEN, stroke_width=5,
                    max_tip_length_to_length_ratio=0.35)
        self.play(GrowArrow(a_e), run_time=0.4)
        self.play(GrowArrow(a_b), FadeIn(blood, shift=UP * 0.1), run_time=0.5)
        self.finish()


class S04Disease(BioScene):
    def construct(self):
        self.add_column("both")
        self.play(*self.focus("right"), run_time=0.7)
        self.at("matching the wrong")
        gly = self.chip_at("wrong-shaped glycogen", GREEN, CX, 2.8, 28)
        self.play(FadeIn(gly, shift=DOWN * 0.1), run_time=0.6)
        self.at("in sick children")
        kids = T("in sick children", 26, GREY).move_to([CX, 2.05, 0])
        self.play(FadeIn(kids, shift=UP * 0.1), run_time=0.4)

        self.at("to specific missing")
        arr = Arrow([CX, 1.75, 0], [CX, 1.0, 0], buff=0, color=GREY, stroke_width=5, max_tip_length_to_length_ratio=0.35)
        matched = T("matched to", 24, GREY).next_to(arr, RIGHT, buff=0.25)
        enz_f = dashed_chip("specific missing enzymes", BLUE, 28).move_to([CX, 0.45, 0])
        self.play(GrowArrow(arr), FadeIn(matched), run_time=0.5)
        self.play(FadeIn(enz_f, shift=UP * 0.1), run_time=0.6)

        self.at("the first proof")
        gold = T("the first proof", 32, GOLD, font=TITLE_FONT).move_to([CX, -0.7, 0])
        gline = Line([CX - 2.6, -1.1, 0], [CX + 2.6, -1.1, 0], color=GOLD, stroke_width=3)
        self.play(FadeIn(gold, shift=UP * 0.1), Create(gline), run_time=0.6)
        self.at("one broken enzyme")
        one = chip("one broken enzyme", BLUE, 28)
        one_f = VGroup(DashedVMobject(one[0], num_dashes=40, dashed_ratio=0.55).set_color(BLUE), one[1])
        one_f.move_to([CX - 2.0, -2.15, 0])
        self.play(FadeIn(one_f, shift=UP * 0.1), run_time=0.5)
        self.at("can cause")
        dis = chip("inherited disease", RED, 28).move_to([CX + 2.6, -2.15, 0])
        a2 = Arrow(one_f.get_right() + RIGHT * 0.1, dis.get_left() + LEFT * 0.1, buff=0, color=GOLD, stroke_width=5,
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

        # --- Carl used the banquet to center Gerty
        self.at("Carl used")
        carl = self.chip_at("Carl", GREY, CX - 2.5, 0.8, 32)
        ban = T("at the banquet", 26, GREY).move_to([CX - 0.2, 1.5, 0])
        self.play(FadeIn(carl, shift=UP * 0.1), FadeIn(ban, shift=UP * 0.1), *self.focus("left"), run_time=0.6)
        self.at("to center")
        gerty = self.chip_at("Gerty", GOLD, CX + 2.7, 0.8, 32)
        arr = Arrow(carl.get_right() + RIGHT * 0.1, gerty.get_left() + LEFT * 0.1, buff=0, color=GOLD, stroke_width=5,
                    max_tip_length_to_length_ratio=0.2)
        cen = T("centered", 26, GOLD).next_to(arr, DOWN, buff=0.15)
        self.play(GrowArrow(arr), FadeIn(gerty, scale=0.9), FadeIn(cen), *self.focus("right"), run_time=0.8)

        # --- the same year: dying of myelofibrosis, finally a full professor
        self.at("The same year", lead=0.4)
        self.play(FadeOut(Group(carl, ban, arr, gerty, cen)), run_time=0.35)
        same = T("the same year", 28, GREY).move_to([CX, 1.35, 0])
        self.play(FadeIn(same, shift=UP * 0.1), run_time=0.4)
        self.at("dying of")
        dy = T("dying of", 26, GREY)
        myel = chip("myelofibrosis", RED, 30)
        row = VGroup(dy, myel).arrange(RIGHT, buff=0.3).move_to([CX, 0.45, 0])
        self.play(FadeIn(dy, shift=UP * 0.1), run_time=0.4)
        self.at("myelofibrosis")
        self.play(FadeIn(myel, shift=UP * 0.1), run_time=0.6)
        self.at("worked through")
        blocks = VGroup(*[Square(0.3, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9) for _ in range(10)])
        blocks.arrange(RIGHT, buff=0.1).move_to([CX, -0.75, 0])
        dec = T("she worked through it for a decade", 26, YELLOW).move_to([CX, -1.45, 0])
        self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in blocks], lag_ratio=0.12), FadeIn(dec), run_time=1.0)
        self.at("she was finally")
        prof = self.chip_at("Gerty: full professor", GOLD, CX, -2.5, 32)
        self.play(FadeIn(prof, shift=UP * 0.1), *self.focus("right"), run_time=0.6)
        self.play(Indicate(prof, color=GOLD, scale_factor=1.05), run_time=0.6)
        self.finish()


class S06Quote(BioScene):
    def construct(self):
        self.add_column("right")
        mark = T("“", 120, GOLD, font=TITLE_FONT)
        l1 = T("It’s free glucose,", 52, TEXT, font=TITLE_FONT)
        l2 = T("it’s free glucose!”", 52, TEXT, font=TITLE_FONT)
        qg = VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        fit(qg, max_w=8.0)
        qg.move_to([CX + 0.1, 0.6, 0])
        mark.scale(0.7).next_to(l1, LEFT, buff=0.12).align_to(l1, UP).shift(UP * 0.12)
        att = T("Gerty Cori", 32, GOLD).next_to(qg, DOWN, buff=0.6).align_to(qg, RIGHT)
        self.play(FadeIn(mark, shift=DOWN * 0.1), run_time=0.6)
        self.play(FadeIn(l1, shift=UP * 0.1), run_time=0.9)
        self.wait(0.5)
        self.play(FadeIn(l2, shift=UP * 0.1), run_time=0.9)
        self.wait(0.5)
        self.play(FadeIn(att, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S07End(BioScene):
    LINE = "Traced the Cori cycle; first tied a missing enzyme to inherited disease."

    def construct(self):
        img, border = portrait(height=2.3, center=(0, 2.0))
        cap = T(CAPTION, 22, GREY).move_to([0, 2.0 - 1.15 - 0.3, 0])
        line = T("Traced the Cori cycle; first tied a missing", 38, font=TITLE_FONT)
        line2 = T("enzyme to inherited disease.", 38, font=TITLE_FONT)
        lg = VGroup(line, line2).arrange(DOWN, buff=0.2).move_to([0, -0.55, 0])
        fit(lg, max_w=11.5)
        sub = T("biochemistrypedia.com", 24, TEAL).move_to([0, -1.85, 0])
        src = T("Source: The Molecule Hunters (v10) · Carl and Gerty Cori profile", 22, GREY).move_to([0, -2.6, 0])
        self.play(FadeIn(img), FadeIn(border), FadeIn(cap), run_time=0.5)
        self.play(FadeIn(lg, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(sub), FadeIn(src), run_time=0.4)
        self.finish()
