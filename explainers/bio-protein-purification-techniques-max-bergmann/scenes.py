"""Max Bergmann: a scientist profile (Biochemistrypedia, protein-purification-techniques lesson).

Narration is the lesson entry's `story`, verbatim. Everything on screen comes from that entry
(name, dates, contribution, story, quote). The portrait is an AI-generated engraving-style
illustration from The Molecule Hunters; it is captioned "illustration · AI-generated" whenever it is
on screen at a readable size. No molecular structure is drawn: proteins are chips, sequences are rows
of numbered/blank tiles, the amino acid table is plain text and bars with no numbers.

COLOR MAP (one color per concept, whole video)
  GOLD   = time and Bergmann himself: name/dates, timeline markers, the Bergmann chip, "first"
  PLACE  (lavender) = places and institutions: the leather-research institute, Rockefeller, the quiet lab
  GREEN  = proteins and their parts: collagen, protein, sequence tiles, amino acid rows
  TEAL   = Bergmann's methods and conviction: carbobenzoxy chemistry, readable sequences, the alphabet,
           amino acid analysis / elementary analysis, "combine their efforts"
  AMBER  = leather
  BLUE   = simpler organic substances (the thing elementary analysis was applied to)
  YELLOW = people he trained and what they did: new recruits, Moore, Stein, Sanger, the Nobel
  RED    = what stood in the way: the Nazi state, expulsion, "could not be read", his death, "did not live to share"
  GREY   = axes, labels, de-emphasized things
"""
import math

import numpy as np
from bp_style import *  # noqa: F401,F403

import os
from pathlib import Path
PORTRAIT = str(Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent / "bergmann_crop.png")
NAME = "Max Bergmann"
DATES = "1886–1944"
CAPTION = "illustration · AI-generated"
PLACE = "#B39DDB"
AMBER = "#E0A458"

INSET_C = np.array([-4.6, 1.2, 0.0])
INSET_H = 3.3
PANEL_C = 1.95


# ----------------------------------------------------------------------------- helpers
def portrait_pair(height):
    img = ImageMobject(PORTRAIT)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["cubic"])
    img.set_height(height)
    frame = Rectangle(width=img.width, height=img.height, stroke_color=GOLD, stroke_width=3, fill_opacity=0)
    return img, frame


def caption_under(frame, size=22):
    return T(CAPTION, size=size, color=GREY, font=TITLE_FONT).next_to(frame, DOWN, buff=0.2)


def name_tag(frame):
    nm = T(NAME, size=34, font=TITLE_FONT)
    dt = T(DATES, size=28, color=GOLD)
    g = VGroup(nm, dt).arrange(DOWN, buff=0.14)
    g.move_to([frame.get_center()[0], frame.get_center()[1] - INSET_H / 2 - 1.3, 0])
    return g


def inset_group():
    img, frame = portrait_pair(INSET_H)
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


def tile(label, color=GREEN, size=0.62, fs=26):
    sq = RoundedRectangle(corner_radius=0.09, width=size, height=size, stroke_color=color, stroke_width=3,
                          fill_color=ManimColor(BG).interpolate(ManimColor(color), 0.2), fill_opacity=1)
    return VGroup(sq, M(str(label), fs, color).move_to(sq))


def cross(center, color=RED, r=0.3, w=8):
    return VGroup(Line([-r, -r, 0], [r, r, 0]), Line([-r, r, 0], [r, -r, 0])).set_color(color).set_stroke(width=w) \
        .move_to(center)


def check(center, color=GREEN, s=0.28, w=8):
    m = VMobject(stroke_color=color, stroke_width=w, fill_opacity=0)
    m.set_points_as_corners([[-s, 0, 0], [-s * 0.3, -s * 0.8, 0], [s, s * 0.9, 0]])
    return m.move_to(center)


def arrow_between(a, b, color=GREY, w=4, buff=0.1):
    return Arrow(a, b, color=color, stroke_width=w, buff=buff, max_tip_length_to_length_ratio=0.3)


class ProfileScene(SpokenScene):
    def add_inset(self):
        img, frame, cap, tag, rule = inset_group()
        self.add(img, frame, cap, tag, rule)


# ----------------------------------------------------------------------------- s00 title
class S00Title(TitleCard):
    LESSON = "Scientist profile"
    TITLE = NAME

    def construct(self):
        img, frame = portrait_pair(4.9)
        grp = Group(img, frame)
        grp.move_to([-3.3, 0.35, 0])
        cap = caption_under(frame, size=24).shift(DOWN * 0.1)
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        name = T(self.TITLE, size=54, font=TITLE_FONT)
        dates = T(DATES, size=38, color=GOLD)
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


# ----------------------------------------------------------------------------- s01 leather = collagen = protein
class S01Leather(ProfileScene):
    def construct(self):
        self.add_inset()
        region = RoundedRectangle(corner_radius=0.2, width=8.2, height=3.0, stroke_color=PLACE, stroke_width=2.5,
                                  fill_color=PLACE, fill_opacity=0.08).move_to([1.95, 1.75, 0])
        region_lab = T("leather-research institute", 28, PLACE)
        region_lab.move_to([region.get_left()[0] + 0.3 + region_lab.width / 2, region.get_top()[1] - 0.4, 0])
        labo = lab(["one of Europe's premier", "protein laboratories"], GREEN, 30).move_to([1.95, 1.2, 0]).set_z_index(2)

        self.at("one of Europe's premier")
        self.play(pop(labo), run_time=0.6)
        self.at("leather research institute")
        self.play(Create(region), FadeIn(region_lab, shift=DOWN * 0.1), run_time=0.8)

        y = -1.55
        leather = lab("leather", AMBER, 32).move_to([-1.0, y, 0])
        collagen = lab("collagen", GREEN, 32).move_to([1.95, y, 0])
        protein = lab("protein", GREEN, 32).move_to([5.0, y, 0])
        a1 = arrow_between(leather.get_right(), collagen.get_left(), GREY)
        a2 = arrow_between(collagen.get_right(), protein.get_left(), GREY)
        is1 = T("is", 26, GREY).next_to(a1, UP, buff=0.12)
        is2 = T("is", 26, GREY).next_to(a2, UP, buff=0.12)
        self.at("because leather")
        self.play(pop(leather), run_time=0.45)
        self.at("is collagen")
        self.play(GrowArrow(a1), FadeIn(is1), pop(collagen), run_time=0.6)
        self.at("and collagen is")
        self.play(GrowArrow(a2), FadeIn(is2), run_time=0.4)
        self.at("protein", nth=1)
        self.play(pop(protein), run_time=0.45)
        # the loop closes: the protein is what the lab studies
        self.play(Indicate(protein, color=GREEN, scale_factor=1.12), Indicate(labo, color=GREEN, scale_factor=1.04),
                  run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- s02 1933, Rockefeller, the conviction
class S021933(ProfileScene):
    def construct(self):
        self.add_inset()
        ay = 2.75
        axis = Arrow([-2.2, ay, 0], [6.15, ay, 0], color=GREY, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.04)
        dot = Dot([-1.2, ay, 0], radius=0.12, color=GOLD)
        date = T("1933", 36, GOLD, weight=BOLD).next_to(dot, UP, buff=0.15).shift(RIGHT * 0.2)
        self.at("in 1933")
        self.play(Create(axis), FadeIn(dot, scale=2), FadeIn(date, shift=UP * 0.1), run_time=0.6)

        nazi = lab("Nazi state", RED, 30).move_to([-0.9, 1.6, 0])
        berg = lab(NAME, GOLD, 30).move_to([4.2, 1.6, 0])
        exp = arrow_between(nazi.get_right(), berg.get_left(), RED, 5)
        exp_lab = T("expelled", 26, RED).next_to(exp, UP, buff=0.1)
        jew = T("for being Jewish", 28, RED).move_to([1.2, 0.85, 0])
        self.at("Nazi state")
        self.play(pop(nazi), run_time=0.45)
        self.at("expelled him")
        self.play(GrowArrow(exp), FadeIn(exp_lab), pop(berg), run_time=0.6)
        self.at("for being Jewish")
        self.play(FadeIn(jew, shift=UP * 0.1), run_time=0.5)

        rock = lab("Rockefeller", PLACE, 30).move_to([4.2, 0.2, 0])
        down = arrow_between(berg.get_bottom(), rock.get_top(), GOLD, 4, 0.08)
        rebuilt = T("rebuilt", 26, GOLD).next_to(down, RIGHT, buff=0.15)
        self.at("he rebuilt")
        self.play(GrowArrow(down), FadeIn(rebuilt), run_time=0.45)
        self.at("Rockefeller")
        self.play(pop(rock), run_time=0.45)

        cbz = lab(["carbobenzoxy", "protecting-group", "chemistry"], TEAL, 26).move_to([-0.1, -1.7, 0])
        conv = lab(["a conviction most chemists", "did not yet share"], TEAL, 26).move_to([3.9, -1.3, 0])
        c1 = arrow_between(cbz.get_top() + RIGHT * 0.9, rock.get_bottom() + LEFT * 0.4, TEAL, 4, 0.08)
        c2 = arrow_between(conv.get_top(), rock.get_bottom() + RIGHT * 0.2, TEAL, 4, 0.08)
        carry = T("carrying", 26, GOLD).next_to(rock, LEFT, buff=0.3)
        self.at("carrying")
        self.play(FadeIn(carry, shift=RIGHT * 0.1), run_time=0.4)
        self.at("carbobenzoxy")
        self.play(pop(cbz), GrowArrow(c1), run_time=0.5)
        self.at("a conviction")
        self.play(pop(conv), GrowArrow(c2), run_time=0.5)
        # "that proteins had readable sequences": the conviction is spelled out, then a row of tiles is read
        conv2 = lab(["proteins have", "readable sequences"], TEAL, 28).move_to(conv)
        tiles = VGroup(*[tile(i + 1, GREEN, 0.52, 22) for i in range(6)]).arrange(RIGHT, buff=0.1)
        tiles.move_to([3.9, -2.75, 0])
        self.at("that proteins had")
        self.play(Transform(conv, conv2), run_time=0.5)
        self.at("readable sequences")
        self.play(LaggedStart(*[FadeIn(t, scale=0.8) for t in tiles], lag_ratio=0.12), run_time=0.7)
        cur = SurroundingRectangle(tiles[0], color=TEAL, buff=0.06, corner_radius=0.1, stroke_width=4)
        self.play(Create(cur), run_time=0.2)
        for t in tiles[1:]:
            self.play(cur.animate.move_to(t), run_time=0.16)
        self.finish()


# ----------------------------------------------------------------------------- s03 count the alphabet first
class S03Alphabet(ProfileScene):
    def construct(self):
        self.add_inset()
        row = VGroup(*[tile("?", GREEN) for _ in range(8)]).arrange(RIGHT, buff=0.12).move_to([3.15, 2.65, 0])
        seq_lab = T("sequence", 30, GREEN).move_to([-1.25, 2.65, 0])
        self.at("sequence could not")
        self.play(pop(seq_lab), LaggedStart(*[FadeIn(t, scale=0.8) for t in row], lag_ratio=0.06), run_time=0.7)
        x = cross(row.get_center(), RED, 0.5, 9).set_z_index(5)
        self.at("not be read")
        self.play(FadeIn(x, scale=1.4), row.animate.set_opacity(0.45), run_time=0.45)

        alpha = lab("alphabet", TEAL, 32).move_to([-0.95, 1.0, 0])
        self.at("alphabet")
        self.play(pop(alpha), run_time=0.5)
        first = T("first", 28, GOLD, weight=BOLD).move_to([-0.95, 1.82, 0])
        self.at("first been")
        self.play(FadeIn(first, shift=DOWN * 0.1), run_time=0.4)
        counted = T("counted", 28, TEAL).next_to(alpha, RIGHT, buff=0.45)
        ck = check(counted.get_right() + RIGHT * 0.45, GREEN, 0.2, 7)
        self.at("been counted")
        self.play(FadeIn(counted, shift=RIGHT * 0.1), Create(ck), run_time=0.5)

        recruits = lab("new recruits", YELLOW, 30).move_to([5.0, 1.0, 0])
        self.at("new recruits")
        self.play(pop(recruits), run_time=0.45)
        arith = T("unglamorous arithmetic", 26, GREY).move_to([4.5, 0.25, 0])
        self.at("unglamorous arithmetic")
        self.play(FadeIn(arith, shift=UP * 0.1), run_time=0.45)

        # the table: name + amount for every amino acid in a protein
        h_name = T("name", 26, GREY).move_to([0.75, -0.55, 0])
        h_amt = T("amount", 26, GREY).move_to([4.3, -0.55, 0])
        rows, bars = [], []
        lens = [3.1, 1.6, 2.4, 0.9]
        for i, ln in enumerate(lens):
            yy = -1.2 - 0.55 * i
            r = T(f"amino acid {i + 1}", 24, GREEN).move_to([0.0, yy, 0], aligned_edge=LEFT)
            r.move_to([r.width / 2 + 0.0, yy, 0])
            rows.append(r)
            b = Rectangle(width=ln, height=0.3, stroke_width=0, fill_color=TEAL, fill_opacity=0.9)
            b.move_to([2.6 + ln / 2, yy, 0])
            bars.append(b)
        dots = VGroup(*[Dot(radius=0.04, color=GREY) for _ in range(3)]).arrange(DOWN, buff=0.1).move_to([0.9, -3.25, 0])
        self.at("naming every amino acid")
        self.play(FadeIn(h_name), LaggedStart(*[pop(r) for r in rows], lag_ratio=0.3), FadeIn(dots), run_time=1.5)
        protein = lab("protein", GREEN, 28).move_to([-1.45, -2.2, 0])
        brace = Line([-0.3, -0.95, 0], [-0.3, -3.0, 0], color=GREY, stroke_width=3)
        self.at("in a protein")
        self.play(pop(protein), Create(brace), run_time=0.45)
        self.at("in what amount")
        self.play(FadeIn(h_amt), LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.2), run_time=0.9)
        self.finish()


# ----------------------------------------------------------------------------- s04 the analogy, then Moore + Stein
class S04Analogy(ProfileScene):
    def construct(self):
        self.add_inset()
        y1, y2 = 1.9, -1.0
        xl, xr = -0.5, 4.3
        aa = lab(["amino acid", "analysis"], TEAL, 30).move_to([xl, y1, 0])
        prot = lab(["proteins", "(macromolecules)"], GREEN, 28).move_to([xr, y1, 0])
        ar1 = arrow_between(aa.get_right(), prot.get_left(), GOLD, 5)
        el = lab(["elementary", "analysis"], TEAL, 30).move_to([xl, y2, 0])
        sub = lab(["simpler organic", "substances"], BLUE, 28).move_to([xr, y2, 0])
        ar2 = arrow_between(el.get_right(), sub.get_left(), GOLD, 5)
        rel = T("= same relationship", 30, GOLD, weight=BOLD).move_to([(xl + xr) / 2, (y1 + y2) / 2, 0])

        self.at("the amino acid analysis")
        self.play(pop(aa), run_time=0.5)
        self.at("proteins", nth=0)
        self.play(pop(prot), run_time=0.5)
        self.at("bore the same relationship")
        self.play(GrowArrow(ar1), run_time=0.5)
        self.at("same relationship")
        self.play(FadeIn(rel, shift=UP * 0.1), run_time=0.5)
        self.at("elementary analysis")
        self.play(pop(el), run_time=0.5)
        self.at("bore to")
        self.play(GrowArrow(ar2), run_time=0.5)
        self.at("simpler organic substances")
        self.play(pop(sub), run_time=0.5)
        glue = VGroup(DashedLine(aa.get_bottom() + DOWN * 0.05, el.get_top() + UP * 0.05, color=GOLD, stroke_width=3,
                                 dash_length=0.1),
                      DashedLine(prot.get_bottom() + DOWN * 0.05, sub.get_top() + UP * 0.05, color=GOLD, stroke_width=3,
                                 dash_length=0.1))
        self.play(Create(glue), Indicate(rel, color=GOLD, scale_factor=1.08), run_time=0.7)
        eq = rel

        # 1939: Moore arrives, Stein is already at the bench
        stage = Group(aa, prot, ar1, el, sub, ar2, rel, glue)
        self.at("When Moore arrived", lead=0.4)
        self.play(FadeOut(stage), run_time=0.4)
        ay = 2.65
        axis = Arrow([-2.2, ay, 0], [6.15, ay, 0], color=GREY, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.04)
        dot = Dot([-1.2, ay, 0], radius=0.12, color=GOLD)
        date = T("1939", 36, GOLD, weight=BOLD).next_to(dot, UP, buff=0.18).shift(RIGHT * 0.2)
        moore = lab("Moore", YELLOW, 32).move_to([-0.8, 0.8, 0])
        stein = lab("Stein", YELLOW, 32).move_to([4.4, 0.8, 0])
        bench_line = Line([3.0, 0.15, 0], [5.8, 0.15, 0], color=GREY, stroke_width=5)
        bench = T("at the bench", 26, GREY).move_to([4.4, -0.3, 0])
        self.at("Moore arrived")
        self.play(FadeIn(moore, shift=RIGHT * 0.4), Create(axis), run_time=0.5)
        self.at("in 1939")
        self.play(FadeIn(dot, scale=2), FadeIn(date, shift=UP * 0.1), run_time=0.45)
        self.at("found Stein")
        self.play(pop(stein), run_time=0.45)
        self.at("at the bench")
        self.play(Create(bench_line), FadeIn(bench, shift=UP * 0.1), run_time=0.5)

        berg = lab(NAME, GOLD, 30).move_to([1.8, -1.9, 0])
        t1 = arrow_between(berg.get_top() + LEFT * 0.4, moore.get_bottom() + RIGHT * 0.2, GOLD, 4, 0.08)
        t2 = arrow_between(berg.get_top() + RIGHT * 0.4, stein.get_bottom() + LEFT * 0.4, GOLD, 4, 0.08)
        self.at("Bergman told them")
        self.play(pop(berg), FadeOut(bench), FadeOut(bench_line), run_time=0.4)
        self.play(GrowArrow(t1), GrowArrow(t2), run_time=0.4)
        self.at("combine")
        self.play(FadeOut(t1), FadeOut(t2),
                  moore.animate.move_to([0.9, 0.8, 0]), stein.animate.move_to([2.9, 0.8, 0]), run_time=0.7)
        join = SurroundingRectangle(Group(moore, stein), color=TEAL, buff=0.2, corner_radius=0.18, stroke_width=3)
        eff = T("combine their efforts", 28, TEAL).next_to(join, UP, buff=0.22)
        told = arrow_between(berg.get_top(), join.get_bottom(), GOLD, 4, 0.08)
        self.play(Create(join), FadeIn(eff, shift=DOWN * 0.1), GrowArrow(told), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s05 1944 and the Nobel
class S05Death(ProfileScene):
    def construct(self):
        self.add_inset()
        ay = 2.65
        axis = Arrow([-2.2, ay, 0], [6.15, ay, 0], color=GREY, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.04)
        dot = Dot([-0.6, ay, 0], radius=0.12, color=GOLD)
        date = T("1944", 36, GOLD, weight=BOLD).next_to(dot, UP, buff=0.18)
        berg = lab(NAME, GOLD, 30).move_to([-0.6, 1.4, 0])
        died = T("died", 28, RED, weight=BOLD).next_to(berg, DOWN, buff=0.2)
        self.add(axis, berg)
        self.at("in 1944")
        self.play(FadeIn(dot, scale=2), FadeIn(date, shift=UP * 0.1), run_time=0.4)
        self.play(FadeIn(died, shift=UP * 0.1), berg.animate.set_opacity(0.55), run_time=0.4)

        sanger = lab(["Sanger's", "insulin sequence"], YELLOW, 28).move_to([4.2, 1.4, 0])
        conv = lab(["proteins have", "readable sequences"], TEAL, 28).move_to([2.2, -0.9, 0])
        self.at("Sanger's insulin")
        self.play(pop(sanger), run_time=0.5)
        self.at("proved him right")
        self.play(pop(conv), run_time=0.45)
        ck = check(conv.get_right() + RIGHT * 0.5, GREEN, 0.3, 9)
        arr = arrow_between(sanger.get_bottom() + LEFT * 0.3, conv.get_top() + RIGHT * 0.9, YELLOW, 4, 0.08)
        self.play(GrowArrow(arr), Create(ck), run_time=0.6)

        # the lab, the two recruits, the Nobel
        stage = Group(axis, dot, date, berg, died, sanger, conv, ck, arr)
        self.at("The quiet lab", lead=0.3)
        self.play(FadeOut(stage), run_time=0.4)
        labc = lab(["the quiet lab"], PLACE, 30).move_to([-0.3, 1.7, 0])
        moore = lab("Moore", YELLOW, 30).move_to([-1.3, -0.35, 0])
        stein = lab("Stein", YELLOW, 30).move_to([0.8, -0.35, 0])
        pair = SurroundingRectangle(Group(moore, stein), color=YELLOW, buff=0.15, corner_radius=0.16, stroke_width=2.5)
        inh = arrow_between(labc.get_bottom(), [(moore.get_center()[0] + stein.get_center()[0]) / 2, pair.get_top()[1], 0],
                            PLACE, 4, 0.08)
        inh_lab = T("inherited", 26, PLACE).next_to(inh, RIGHT, buff=0.2)
        self.at("The quiet lab")
        self.play(pop(labc), run_time=0.45)
        self.at("two recruits")
        self.play(pop(moore), pop(stein), Create(pair), run_time=0.5)
        self.at("inherited")
        self.play(GrowArrow(inh), FadeIn(inh_lab), run_time=0.5)

        nobel = lab("the Nobel", GOLD, 36).move_to([4.3, -0.35, 0])
        win = arrow_between(pair.get_right(), nobel.get_left(), YELLOW, 5)
        self.at("win the Nobel")
        self.play(GrowArrow(win), pop(nobel), run_time=0.6)

        berg2 = lab(NAME, GOLD, 30).move_to([-0.3, -2.4, 0]).set_opacity(0.55)
        no = DashedLine(berg2.get_right() + RIGHT * 0.1, [nobel.get_bottom()[0] - 0.3, nobel.get_bottom()[1] - 0.1, 0],
                        color=RED, stroke_width=4, dash_length=0.12)
        xm = cross(no.get_center(), RED, 0.2, 7)
        share = T("did not live to share", 28, RED).move_to([4.3, -2.6, 0])
        self.at("he did not live")
        self.play(pop(berg2), Create(no), run_time=0.5)
        self.play(FadeIn(xm, scale=1.5), FadeIn(share, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s06 the quote
class S06Quote(ProfileScene):
    def construct(self):
        self.add_inset()
        lines = ["“The amino acid analysis of", "proteins bore the same relationship", "to these macromolecules that",
                 "elementary analysis bore to the", "chemistry of simpler organic", "substances.”"]
        # every line carries an invisible "Hgj" tail so all line boxes share one ascender/descender height
        q = VGroup(*[T(l + " Hgj", 36, TEXT, font=TITLE_FONT, t2c={" Hgj": BG}) for l in lines]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2)
        fit(q, max_w=8.4, max_h=5.2)
        tailw = T(" Hgj", 36, TEXT, font=TITLE_FONT).width
        vis_w = max(ln.width for ln in q) - tailw
        who = T("— Max Bergmann", 32, GOLD)
        who.next_to(q, DOWN, buff=0.45)
        who.align_to([q.get_left()[0] + vis_w, 0, 0], RIGHT)
        g = VGroup(q, who)
        g.shift(RIGHT * (PANEL_C - (q.get_left()[0] + vis_w / 2)))
        g.shift(UP * (0.0 - g.get_center()[1]))
        for ln in q:
            ln.set_opacity(0)
        who.set_opacity(0)
        self.add(g)
        self.wait(0.3)
        for ln in q:
            self.play(ln.animate.set_opacity(1.0), run_time=0.55)
        self.wait(0.4)
        self.play(who.animate.set_opacity(1.0), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s07 end card
class S07End(EndCard):
    LINE = "Made amino acid analysis quantitative; showed enzyme specificity with synthetic substrates."

    def construct(self):
        a = T("Made amino acid analysis quantitative;", size=38, font=TITLE_FONT)
        b = T("showed enzyme specificity with synthetic substrates.", size=38, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.22)
        fit(line, max_w=12.0)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
