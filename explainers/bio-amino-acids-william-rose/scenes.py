"""William Rose: a scientist profile (Biochemistrypedia, amino-acids lesson).

Narration is the lesson entry's `story`, verbatim. Everything on screen comes from that entry
(name, dates, contribution, story, quote). The portrait is an AI-generated engraving-style
illustration from The Molecule Hunters; it is captioned "illustration · AI-generated" whenever it is
on screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = Rose himself: name, dates, portrait frame, the line he drew
  TEAL   = the amino acids (tiles in the alphabet grid, the diet, the mixture)
  GREEN  = threonine, the one that was found
  RED    = what was missing or went wrong: the empty slot, wasting, the sulfurous taste, what broke a human
  YELLOW = years and "decades later" (1935; histidine added later)
  PLACE (lavender) = places and institutions: the Illinois lab, the fractionation works
  CREAM  = casein / milk protein
  AMBER  = corn protein
  PURPLE = the sugar threose
  PINK   = the peppermint candy
  ORANGE = the amino acids an adult cannot live without and has to eat
  TEXT (white) = the test subjects (rats, graduate students)
  GREY   = labels, apparatus, de-emphasized things
No molecular structure is drawn: every amino acid is a plain labelled tile, the sugar is a chip,
the mill is two rollers in a box.
"""
import math
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

PORTRAIT = str(Path(__file__).resolve().parent / "portrait_crop.png")
PORTRAIT_INSET = str(Path(__file__).resolve().parent / "portrait_inset.png")   # pre-downsampled: no moire on the engraving stipple
CAPTION = "illustration · AI-generated"
PLACE = "#B39DDB"
AMBER = "#E0A458"
PURPLE = "#B58CD9"
PINK = "#F06292"
ORANGE = "#E8913A"
CREAM = "#EFE3C8"

INSET_C = np.array([-4.6, 1.15, 0.0])
INSET_H = 3.2
PANEL_C = 1.95


def mix(color, k=0.22):
    return ManimColor(BG).interpolate(ManimColor(color), k)


def portrait_pair(height, src=None):
    img = ImageMobject(src or PORTRAIT)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["cubic"])
    img.set_height(height)
    frame = Rectangle(width=img.width, height=img.height, stroke_color=GOLD, stroke_width=3, fill_opacity=0)
    return img, frame


def caption_under(frame, size=22):
    return T(CAPTION, size=size, color=GREY, font=TITLE_FONT).next_to(frame, DOWN, buff=0.2)


def name_tag(frame):
    nm = T("William Rose", size=34, font=TITLE_FONT)
    dt = T("1887–1985", size=28, color=GOLD)
    g = VGroup(nm, dt).arrange(DOWN, buff=0.14)
    g.move_to([frame.get_center()[0], frame.get_center()[1] - INSET_H / 2 - 1.3, 0])
    return g


def inset_group():
    img, frame = portrait_pair(INSET_H, PORTRAIT_INSET)
    img.move_to(INSET_C)
    frame.move_to(INSET_C)
    cap = caption_under(frame)
    tag = name_tag(frame)
    rule = Line([-2.7, -3.2, 0], [-2.7, 3.2, 0], color=GREY, stroke_width=1.5).set_opacity(0.35)
    return img, frame, cap, tag, rule


def lab(lines, color=BLUE, size=28, pad=0.22, fill=0.16):
    if isinstance(lines, str):
        lines = [lines]
    txt = VGroup(*[T(l, size, color) for l in lines]).arrange(DOWN, buff=0.1)
    ref_h = len(lines) * T("Ag", size).height + (len(lines) - 1) * 0.1
    box = RoundedRectangle(corner_radius=0.14, width=txt.width + 2 * pad, height=max(txt.height, ref_h) + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=fill)
    return VGroup(box, txt.move_to(box))


def pop(mob):
    return FadeIn(mob, shift=UP * 0.12)


def tile(color=TEAL, size=0.5):
    return RoundedRectangle(corner_radius=0.08, width=size, height=size, stroke_color=color, stroke_width=2.5,
                            fill_color=mix(color), fill_opacity=1)


def empty_slot(size=0.5, color=RED):
    d = DashedVMobject(RoundedRectangle(corner_radius=0.08, width=size, height=size, stroke_color=color,
                                        stroke_width=2.5), num_dashes=24, dashed_ratio=0.55)
    q = M("?", int(size * 52), color)
    q.move_to(d)
    return VGroup(d, q)


def grid_pos(center, pitch, cols=10, n=20):
    rows = math.ceil(n / cols)
    out = []
    for i in range(n):
        r, c = divmod(i, cols)
        out.append(np.array([center[0] + (c - (cols - 1) / 2) * pitch,
                             center[1] + ((rows - 1) / 2 - r) * pitch, 0.0]))
    return out


def person(color=TEXT, s=1.0):
    head = Circle(radius=0.15 * s, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.35)
    body = RoundedRectangle(corner_radius=0.12 * s, width=0.46 * s, height=0.3 * s, stroke_color=color,
                            stroke_width=3, fill_color=color, fill_opacity=0.2)
    head.move_to(UP * 0.28 * s)
    body.move_to(DOWN * 0.05 * s)
    return VGroup(head, body)


class ProfileScene(SpokenScene):
    def add_inset(self):
        img, frame, cap, tag, rule = inset_group()
        self.add(img, frame, cap, tag, rule)

    def until(self, t):
        rest = t - self.elapsed()
        if rest > 0.02:
            self.wait(rest)


# ----------------------------------------------------------------------------- s00 title
class S00Title(TitleCard):
    LESSON = "Scientist profile"
    TITLE = "William Rose"

    def construct(self):
        img, frame = portrait_pair(4.7)
        grp = Group(img, frame)
        grp.move_to([-3.3, 0.35, 0])
        cap = caption_under(frame, size=24).shift(DOWN * 0.15)
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        name = T(self.TITLE, size=54, font=TITLE_FONT)
        dates = T("1887–1985", size=38, color=GOLD)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        txt = VGroup(brand, lesson, name, dates, rule).arrange(DOWN, buff=0.3).move_to([3.1, 0.2, 0])
        self.play(FadeIn(img), FadeIn(frame), FadeIn(cap), run_time=0.5)
        self.play(
            ScaleInPlace(grp, 1.07, run_time=2.0, rate_func=linear),
            Succession(
                FadeIn(VGroup(brand, lesson), shift=UP * 0.1, run_time=0.4),
                Write(name, run_time=0.7),
                FadeIn(dates, shift=UP * 0.1, run_time=0.4),
                GrowFromCenter(rule, run_time=0.3),
            ),
        )
        i_img, i_frame, i_cap, i_tag, i_rule = inset_group()
        self.play(
            FadeOut(txt), FadeOut(cap),
            img.animate.set_height(INSET_H).move_to(INSET_C), frame.animate.become(i_frame),
            run_time=0.7,
        )
        self.play(FadeIn(i_cap), FadeIn(i_tag), FadeIn(i_rule), run_time=0.25)
        self.finish()


# ----------------------------------------------------------------------------- s01 the alphabet
class S01Alphabet(ProfileScene):
    def construct(self):
        self.add_inset()
        ms = lab("minister's son", GOLD, 28)
        la = lab("Latin", GREY, 28)
        gr = lab("Greek", GREY, 28)
        top = VGroup(ms, la, gr).arrange(RIGHT, buff=0.3).move_to([PANEL_C, 2.85, 0])
        self.at("minister's", lead=0.0)
        self.play(pop(ms), run_time=0.45)
        self.at("Latin")
        self.play(pop(la), run_time=0.4)
        self.at("Greek")
        self.play(pop(gr), run_time=0.4)

        # the alphabet, one letter short
        pos = grid_pos([PANEL_C, 0.95], 0.62)
        tiles = [tile(TEAL, 0.5).move_to(p) for p in pos[:19]]
        slot = empty_slot(0.5).move_to(pos[19])
        self.at("Rose", lead=0.0)
        alpha = T("an alphabet", 28, GREY).move_to([PANEL_C, 0.0, 0])
        self.play(LaggedStart(*[FadeIn(t, scale=0.6) for t in tiles], lag_ratio=0.04, run_time=0.9),
                  FadeIn(alpha, shift=UP * 0.1, run_time=0.9))
        self.at("short one", lead=0.1)
        short = T("one letter short", 32, RED).move_to([PANEL_C, -0.65, 0])
        self.play(FadeIn(slot, scale=1.4), FadeIn(short, shift=UP * 0.1), run_time=0.6)
        self.at("intolerable", lead=0.15)
        intol = T("intolerable", 46, RED, font=TITLE_FONT).move_to([PANEL_C, -1.9, 0])
        self.play(Write(intol), Indicate(slot, color=RED, scale_factor=1.35), run_time=0.8)

        # rats on the synthetic diet
        self.at("He fed rats", lead=0.4)
        grid = VGroup(*tiles, slot)
        self.play(FadeOut(VGroup(top, alpha, short, intol)),
                  grid.animate.scale(0.78).move_to([0.6, 2.25, 0]), run_time=0.6)
        diet = T("fully synthetic diet", 28, TEAL).move_to([0.6, 3.1, 0])
        rats = lab("rats", TEXT, 28).move_to([-1.0, 0.5, 0])
        outline = Rectangle(width=5.2, height=0.42, stroke_color=GREY, stroke_width=3).move_to([3.3, 0.5, 0])
        v = ValueTracker(1.0)

        def fill():
            k = v.get_value()
            r = Rectangle(width=max(0.02, 5.2 * k), height=0.42, stroke_width=0, fill_opacity=0.9,
                          fill_color=interpolate_color(ManimColor(RED), ManimColor(TEXT), k))
            return r.move_to([outline.get_left()[0] + r.width / 2, 0.5, 0])

        bar = always_redraw(fill)
        self.play(pop(rats), run_time=0.35)
        self.at("synthetic diet", lead=0.3)
        self.play(FadeIn(diet, shift=DOWN * 0.1), run_time=0.4)
        self.at("all 19", lead=0.3)
        n19 = VGroup(M("19", 54, TEAL), T("then-known", 24, GREY)).arrange(DOWN, buff=0.08).move_to([5.0, 2.25, 0])
        self.play(FadeIn(n19, shift=LEFT * 0.2), run_time=0.5)
        self.at("amino acids", lead=0.1)
        self.play(Indicate(grid, color=TEAL, scale_factor=1.05), run_time=0.7)
        self.at("watched", lead=0.1)
        self.play(FadeIn(outline), FadeIn(bar), run_time=0.5)
        self.at("waste", lead=0.1)
        wd = T("waste", 30, RED).move_to([1.2, -0.3, 0])
        self.play(v.animate.set_value(0.3), FadeIn(wd, shift=UP * 0.1), run_time=0.9, rate_func=linear)
        self.at("die", lead=0.1)
        wd2 = T("and die", 30, RED).next_to(wd, RIGHT, buff=0.2).align_to(wd, DOWN)
        self.play(v.animate.set_value(0.0), FadeIn(wd2, shift=UP * 0.1), run_time=0.5, rate_func=linear)
        self.at("plenty", lead=0.1)
        plenty = T("in the middle of plenty", 28, TEAL).move_to([0.6, 1.4, 0])
        self.play(FadeIn(plenty, shift=UP * 0.1), Indicate(grid, color=TEAL, scale_factor=1.04), run_time=0.8)

        self.at("proof", lead=0.15)
        ring = Circle(radius=0.25, color=RED, stroke_width=4).move_to(slot)
        t1 = T("something essential", 40, RED, font=TITLE_FONT).move_to([PANEL_C, -1.45, 0])
        t2 = T("was still missing", 40, RED, font=TITLE_FONT).move_to([PANEL_C, -2.3, 0])
        self.play(Create(ring), Indicate(slot, color=RED, scale_factor=1.5), run_time=0.7)
        self.at("something essential", lead=0.1)
        self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.6)
        self.at("still", lead=0.1)
        self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s02 threonine
class S02Threonine(ProfileScene):
    def construct(self):
        self.add_inset()
        # --- A: the lab becomes a fractionation works, grinding milk protein
        lab1 = lab("Illinois lab", PLACE, 30).move_to([PANEL_C, 2.9, 0])
        self.at("Illinois", lead=0.1)
        self.play(pop(lab1), run_time=0.5)
        self.at("fractionation", lead=0.2)
        lab2 = lab("fractionation works", PLACE, 30).move_to([PANEL_C, 2.9, 0])
        self.play(Transform(lab1, lab2), run_time=0.7)

        box = RoundedRectangle(corner_radius=0.15, width=1.9, height=1.3, stroke_color=GREY, stroke_width=3,
                               fill_color=mix(GREY, 0.2), fill_opacity=1)
        r1 = Circle(radius=0.3, stroke_color=GREY, stroke_width=3).move_to(box.get_center() + LEFT * 0.4)
        r2 = Circle(radius=0.3, stroke_color=GREY, stroke_width=3).move_to(box.get_center() + RIGHT * 0.4)
        s1 = Line(r1.get_center() + UP * 0.3, r1.get_center() + DOWN * 0.3, color=GREY, stroke_width=3)
        s2 = Line(r2.get_center() + UP * 0.3, r2.get_center() + DOWN * 0.3, color=GREY, stroke_width=3)
        mill = VGroup(box, r1, r2, s1, s2).move_to([2.2, 0.9, 0])
        grind_l = T("grinding", 26, GREY).next_to(mill, UP, buff=0.15)
        milk = lab("milk protein", CREAM, 28).move_to([-0.7, 0.9, 0])
        a1 = Arrow(milk.get_right() + RIGHT * 0.05, mill.get_left() + LEFT * 0.05, buff=0, color=GREY, stroke_width=4,
                   max_tip_length_to_length_ratio=0.3)
        bars = VGroup(*[Rectangle(width=1.3, height=0.17, stroke_width=0, fill_color=GREY, fill_opacity=0.65)
                        for _ in range(5)]).arrange(DOWN, buff=0.1).move_to([5.1, 0.9, 0])
        a2 = Arrow(mill.get_right() + RIGHT * 0.05, bars.get_left() + LEFT * 0.1, buff=0, color=GREY, stroke_width=4,
                   max_tip_length_to_length_ratio=0.3)
        self.at("grinding", lead=0.1)
        self.play(FadeIn(mill, scale=0.8), FadeIn(grind_l), run_time=0.5)
        self.play(Rotate(VGroup(r1, s1), angle=-2 * PI, about_point=r1.get_center(), run_time=1.2, rate_func=linear),
                  Rotate(VGroup(r2, s2), angle=2 * PI, about_point=r2.get_center(), run_time=1.2, rate_func=linear),
                  AnimationGroup(pop(milk), GrowArrow(a1), GrowArrow(a2), FadeIn(bars), lag_ratio=0.3, run_time=1.2))
        self.at("kilogram", lead=0.3)
        pile = VGroup(*[Square(0.3, stroke_width=0, fill_color=CREAM, fill_opacity=0.85) for _ in range(12)])
        pile.arrange_in_grid(rows=3, cols=4, buff=0.08).move_to([-0.7, -0.85, 0])
        kg = T("by the kilogram", 28, GREY).move_to([-0.7, -1.85, 0])
        self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in pile], lag_ratio=0.04), FadeIn(kg), run_time=0.5)
        self.play(LaggedStart(*[b.animate.move_to([2.2, 0.9, 0]).set_opacity(0) for b in pile], lag_ratio=0.05),
                  Rotate(VGroup(r1, s1), angle=-PI, about_point=r1.get_center(), rate_func=linear),
                  Rotate(VGroup(r2, s2), angle=PI, about_point=r2.get_center(), rate_func=linear),
                  run_time=0.7)
        gold = bars[2]
        self.play(gold.animate.set_fill(GOLD, 1.0), run_time=0.3)

        # --- B: casein held it, corn protein lacked it
        self.at("casein", lead=0.45)
        self.play(FadeOut(VGroup(lab1, mill, grind_l, milk, a1, a2, bars, pile, kg)), run_time=0.35)
        pitch = 0.56
        xs = [0.9 + pitch * i for i in range(9)]
        casein = lab("casein", CREAM, 28).move_to([-0.95, 2.0, 0])
        ctiles = VGroup(*[tile(TEAL, 0.46).move_to([xs[i], 2.0, 0]) for i in range(8)])
        q_t = tile(GOLD, 0.46).move_to([xs[8], 2.0, 0])
        q_q = M("?", 26, GOLD).move_to(q_t)
        q = VGroup(q_t, q_q)
        held = T("whatever casein held", 26, GOLD).move_to([5.0, 2.75, 0])
        held.set_x(min(held.get_x(), 6.2 - held.width / 2))
        self.play(pop(casein), LaggedStart(*[FadeIn(t, scale=0.6) for t in ctiles], lag_ratio=0.04),
                  Succession(Wait(0.4), AnimationGroup(FadeIn(q, scale=1.3), FadeIn(held, shift=DOWN * 0.1))),
                  run_time=0.8)
        self.at("corn protein", lead=0.25)
        corn = lab("corn protein", AMBER, 28).move_to([-0.95, 0.85, 0])
        ktiles = VGroup(*[tile(TEAL, 0.46).move_to([xs[i], 0.85, 0]) for i in range(8)])
        gap = empty_slot(0.46).move_to([xs[8], 0.85, 0])
        self.play(pop(corn), LaggedStart(*[FadeIn(t, scale=0.6) for t in ktiles], lag_ratio=0.04),
                  Succession(Wait(0.4), FadeIn(gap, scale=1.3)), run_time=0.7)
        self.at("lacked", lead=0.1)
        link = DashedLine(q_t.get_bottom() + DOWN * 0.05, gap.get_top() + UP * 0.05, color=RED, stroke_width=3)
        lacked = T("lacked", 26, RED).next_to(gap, DOWN, buff=0.15)
        self.play(Create(link), FadeIn(lacked, shift=UP * 0.1), run_time=0.6)

        # --- C: 1935, threonine, and its name
        self.at("in 1935", lead=0.1)
        yr = M("1935", 46, YELLOW).move_to([-1.0, -0.9, 0])
        arr = Arrow([-0.1, -0.9, 0], [3.5, -0.9, 0], buff=0, color=GREY, stroke_width=4,
                    max_tip_length_to_length_ratio=0.12)
        self.play(Write(yr), run_time=0.6)
        self.play(GrowArrow(arr, rate_func=linear), run_time=1.3)
        self.at("crystallized", lead=0.1)
        cry = T("his team crystallized it", 26, GREY).move_to([1.7, -0.45, 0])
        self.play(FadeIn(cry, shift=UP * 0.1), run_time=0.5)
        self.until(self.t_of("crystallized") + 0.75)
        thr = lab("threonine", GREEN, 32).move_to([4.9, -0.9, 0])
        self.play(pop(thr),
                  q_t.animate.set_stroke(GREEN).set_fill(mix(GREEN, 0.35), 1.0),
                  FadeOut(q_q), FadeOut(held), run_time=0.6)
        self.play(Indicate(thr, color=GREEN, scale_factor=1.08), run_time=0.5)
        self.until(self.t_of("for its") - 1.0)
        thro = lab("threose", PURPLE, 30).move_to([4.9, -2.7, 0])
        sug = T("the sugar", 26, GREY).next_to(thro, LEFT, buff=0.3)
        ar2 = DashedLine(thr.get_bottom() + DOWN * 0.05, thro.get_top() + UP * 0.05, color=PURPLE, stroke_width=4)
        ar2.add_tip(tip_length=0.2)
        echo = T("named for its structural echo", 26, GREY).move_to([2.15, -1.8, 0])
        echo.set_x(min(echo.get_x(), 4.3 - echo.width / 2))
        self.play(Create(ar2), pop(thro), run_time=0.6)
        self.at("structural echo", lead=0.1)
        self.play(FadeIn(echo, shift=UP * 0.1), run_time=0.5)
        self.at("sugar", lead=0.1)
        self.play(FadeIn(sug, shift=RIGHT * 0.1), run_time=0.4)
        self.finish()


# ----------------------------------------------------------------------------- s03 graduate students
class S03Students(ProfileScene):
    def construct(self):
        self.add_inset()
        rats = lab("rats", TEXT, 26).move_to([-0.8, 2.75, 0])
        rats.set_opacity(0.5)
        self.add(rats)
        self.at("moved the experiment", lead=0.2)
        stu = lab(["healthy male", "graduate students"], TEXT, 28).move_to([3.5, 2.55, 0])
        arr = Arrow(rats.get_right() + RIGHT * 0.1, stu.get_left() + LEFT * 0.1, buff=0, color=GREY, stroke_width=4,
                    max_tip_length_to_length_ratio=0.2)
        self.play(GrowArrow(arr), pop(stu), run_time=0.7)
        self.at("healthy male", lead=0.0)
        people = VGroup(*[person(TEXT) for _ in range(4)]).arrange(RIGHT, buff=0.35).move_to([3.5, 1.3, 0])
        self.play(LaggedStart(*[pop(p) for p in people], lag_ratio=0.2), run_time=0.9)

        # masking the taste
        self.at("masking", lead=0.1)
        mixc = lab("amino acid mixture", TEAL, 28).move_to([1.0, -0.3, 0])
        self.play(pop(mixc), run_time=0.5)
        self.at("sulphurous", lead=0.1)
        sulf = T("sulfurous taste", 28, RED).move_to([1.0, 0.55, 0])
        waves = VGroup(*[Arc(radius=0.2, start_angle=PI / 2, angle=-PI, color=RED, stroke_width=3)
                         .move_to([mixc.get_center()[0] - 1.0 + 0.5 * i, 0.55, 0]).rotate(PI / 2) for i in range(5)])
        self.play(FadeIn(sulf, shift=UP * 0.1), run_time=0.5)
        self.at("peppermint", lead=0.15)
        candy = VGroup(Circle(radius=0.42, stroke_color=PINK, stroke_width=4, fill_color=mix(PINK, 0.5), fill_opacity=1))
        stripes = VGroup(*[Line([-hw, d - 0.12, 0], [hw, d + 0.12, 0], color=TEXT, stroke_width=4)
                           for d, hw in ((-0.2, 0.24), (0.0, 0.34), (0.2, 0.24))])
        stripes.set_opacity(0.7)
        candy_g = VGroup(candy[0], stripes).move_to([4.6, -1.5, 0])
        cl = T("peppermint candy", 28, PINK).next_to(candy_g, DOWN, buff=0.15)
        self.play(FadeIn(candy_g, scale=0.6), FadeIn(cl, shift=UP * 0.1), run_time=0.6)
        self.at("candy", lead=0.15)
        masked = T("masked", 28, PINK).move_to([mixc.get_right()[0] + 0.55, -1.15, 0])
        self.play(candy_g.animate.move_to([mixc.get_right()[0] + 0.55, -0.3, 0]), FadeOut(cl), FadeIn(masked),
                  sulf.animate.set_opacity(0.3), run_time=0.6)

        # pulling out one at a time
        self.at("pulling", lead=0.2)
        self.play(FadeOut(VGroup(mixc, sulf, candy_g, masked)), run_time=0.4)
        pos = grid_pos([PANEL_C, -0.45], 0.62)
        tiles = [tile(TEAL, 0.5).move_to(p) for p in pos]
        self.play(LaggedStart(*[FadeIn(t, scale=0.6) for t in tiles], lag_ratio=0.02), run_time=0.5)
        self.at("one amino acid at a time", lead=0.0)
        order = [3, 12, 7, 16, 1, 9]
        for i in order:
            t = tiles[i]
            home = pos[i]
            self.play(t.animate.move_to(home + UP * 0.9).set_opacity(0.0), run_time=0.17)
            self.play(t.animate.move_to(home).set_opacity(1.0), run_time=0.17)
        self.at("which removals", lead=0.1)
        ask = T("which removals broke a grown human?", 32, RED).move_to([PANEL_C, -2.35, 0])
        self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.5)
        self.at("broke", lead=0.1)
        p = people[2]
        self.play(p.animate.set_color(RED), Indicate(p, color=RED, scale_factor=1.3), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- s04 the line at eight
class S04Eight(ProfileScene):
    def construct(self):
        self.add_inset()
        pos = grid_pos([PANEL_C, 1.0], 0.62)
        tiles = [tile(TEAL, 0.5).move_to(p) for p in pos]
        self.play(LaggedStart(*[FadeIn(t, scale=0.6) for t in tiles], lag_ratio=0.02), run_time=0.5)
        sub = T("patient subtraction", 36, GOLD, font=TITLE_FONT).move_to([PANEL_C, 2.6, 0])
        self.at("patient", lead=0.1)
        self.play(FadeIn(sub, shift=DOWN * 0.1), run_time=0.5)
        for i in (5, 14):
            self.play(tiles[i].animate.shift(UP * 0.7).set_opacity(0.0), run_time=0.22)
            self.play(tiles[i].animate.shift(DOWN * 0.7).set_opacity(1.0), run_time=0.22)

        eight = [1, 3, 4, 8, 10, 12, 15, 17]
        hist = 9
        self.at("which amino acids", lead=0.1)
        learned = T("which amino acids an adult …", 32, GREY).move_to([PANEL_C, 2.6, 0])
        self.play(FadeOut(sub), FadeIn(learned, shift=DOWN * 0.1), run_time=0.5)
        self.at("cannot live without", lead=0.2)
        must = T("cannot live without", 34, ORANGE).move_to([PANEL_C, 2.6, 0])
        self.play(FadeIn(must, shift=DOWN * 0.1),
                  *[tiles[i].animate.set_stroke(ORANGE).set_fill(mix(ORANGE, 0.3), 1.0) for i in eight],
                  FadeOut(learned), run_time=0.9)

        self.at("has to eat", lead=0.1)
        must2 = fit(T("cannot live without and has to eat", 34, ORANGE), max_w=8.6).move_to([PANEL_C, 2.6, 0])
        self.play(Transform(must, must2), run_time=0.6)

        # the line at eight
        self.at("line at 8", lead=0.3)
        newpos = {}
        top_y, line_y = 1.9, 0.95
        row8 = [np.array([-1.35 + 0.62 * k, top_y, 0]) for k in range(9)]
        rest = [i for i in range(20) if i not in eight]
        for k, i in enumerate(eight):
            newpos[i] = row8[k]
        for k, i in enumerate(rest):
            r, c = divmod(k, 6)
            newpos[i] = np.array([-1.35 + 0.62 * c, 0.3 - 0.62 * r, 0.0])
        self.play(*[tiles[i].animate.move_to(newpos[i]) for i in range(20)], FadeOut(must), run_time=1.0)
        line = Line([-1.9, line_y, 0], [3.2, line_y, 0], color=GOLD, stroke_width=5)
        n8 = M("8", 80, ORANGE).move_to([4.9, top_y, 0])
        rl = T("Rose's line", 26, GOLD).move_to([4.9, line_y, 0])
        self.play(Create(line), FadeIn(n8, scale=1.3), FadeIn(rl), run_time=0.7)

        # histidine, decades later
        self.at("histidine", lead=0.1)
        hl = T("histidine", 28, YELLOW).move_to([4.6, -0.3, 0])
        harr = Arrow(hl.get_left() + LEFT * 0.05, tiles[hist].get_right() + RIGHT * 0.12, buff=0, color=YELLOW,
                     stroke_width=4, max_tip_length_to_length_ratio=0.25)
        self.play(tiles[hist].animate.set_stroke(YELLOW).set_fill(mix(YELLOW, 0.35), 1.0),
                  FadeIn(hl, shift=LEFT * 0.1), GrowArrow(harr), run_time=0.6)
        self.at("decades later", lead=0.1)
        later = T("decades later", 28, YELLOW).move_to([4.6, -1.0, 0])
        self.play(FadeOut(harr), FadeIn(later, shift=UP * 0.1),
                  tiles[hist].animate.move_to(row8[8]), run_time=1.0)
        self.at("make the modern", lead=0.1)
        n9 = M("9", 80, YELLOW).move_to(n8)
        mod = T("the modern nine", 40, YELLOW, font=TITLE_FONT).move_to([PANEL_C, -2.4, 0])
        self.play(Transform(n8, n9), FadeIn(mod, shift=UP * 0.1), run_time=0.7)
        self.play(Indicate(n8, color=YELLOW, scale_factor=1.2), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s05 quote
class S05Quote(ProfileScene):
    def construct(self):
        self.add_inset()
        lines = ["“It was obvious from this, that casein", "must contain an amino acid, not present",
                 "in zein and then unknown, that was", "essential for life.”"]
        q = VGroup(*[T(l, 38, TEXT, font=TITLE_FONT) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        fit(q, max_w=8.4)
        who = T("— William Rose", 32, GOLD)
        g = VGroup(q, who).arrange(DOWN, aligned_edge=RIGHT, buff=0.55).move_to([PANEL_C, 0.1, 0])
        for ln in q:
            ln.set_opacity(0)
        who.set_opacity(0)
        self.add(g)
        self.wait(0.4)
        for ln in q:
            self.play(ln.animate.set_opacity(1.0), run_time=0.8)
        self.wait(0.5)
        self.play(who.animate.set_opacity(1.0), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s06 end card
class S06End(EndCard):
    LINE = "Discovered threonine, the last amino acid; mapped which ones humans must eat."

    def construct(self):
        a = T("Discovered threonine, the last amino acid;", size=42, font=TITLE_FONT)
        b = T("mapped which ones humans must eat.", size=42, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.22)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
