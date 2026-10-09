"""Emil Fischer: a scientist profile (Biochemistrypedia, carbohydrates lesson).

Narration is the lesson entry's `story`, verbatim. Everything on screen comes from that entry
(name, dates, contribution, story, quotes). The portrait is an AI-generated engraving-style
illustration from The Molecule Hunters; it is captioned "illustration · AI-generated" whenever it is
on screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = Fischer himself: portrait frame, "most exacting", what he invented (projection, D/L, lock and key)
  YELLOW = years (1880s, 1890s, 1919)
  ORANGE = laboratory methods and reagents (osazones, oxidation, cyanohydrin chain-extension, phenylhydrazine)
  GREEN  = the sugars
  TEAL   = reading structure: deduction, the hydroxyl question, three-dimensional bookkeeping
  BLUE   = proteins, enzymes and lectins
  RED    = what stood in the way or did harm (too dull, no instrument, poison)
  PLACE (lavender) = Germany
  GREY   = labels, the instrument, de-emphasized things
No molecular structure is drawn: the sugars are plain tiles, the lock and key are generic polygons labelled
"protein" and "sugar", the 3-D bookkeeping is an empty box.
"""
import math

import numpy as np
from bp_style import *  # noqa: F401,F403

config.disable_caching = True

from pathlib import Path
import os

PORTRAIT = str(Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent / "fischer_crop.png")
CAPTION = "illustration · AI-generated"
NAME = "Emil Fischer"
DATES = "1852–1919"
PLACE = "#B39DDB"       # places
ORANGE = "#F2994A"      # lab methods and reagents

INSET_C = np.array([-4.6, 1.15, 0.0])
INSET_H = 3.2
PX = 1.95               # x center of the right panel (x from -2.4 to 6.3)


# ----------------------------------------------------------------------------- helpers
def portrait_pair(height):
    img = ImageMobject(PORTRAIT).set_height(height)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["cubic"])
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
    """Chip with one or more centered lines of text."""
    if isinstance(lines, str):
        lines = [lines]
    txt = VGroup(*[T(l, size, color) for l in lines]).arrange(DOWN, buff=0.1)
    ref_h = len(lines) * T("Ag", size).height + (len(lines) - 1) * 0.1
    box = RoundedRectangle(corner_radius=0.14, width=txt.width + 2 * pad, height=max(txt.height, ref_h) + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=fill)
    return VGroup(box, txt.move_to(box))


def pop(mob):
    return FadeIn(mob, shift=UP * 0.12)


def cross_at(pt, size=0.22, color=RED, width=8):
    return VGroup(Line([-size, -size, 0], [size, size, 0]), Line([-size, size, 0], [size, -size, 0])) \
        .set_color(color).set_stroke(width=width).move_to(pt)


class ProfileScene(SpokenScene):
    def add_inset(self):
        img, frame, cap, tag, rule = inset_group()
        self.add(img, frame, cap, tag, rule)


# ----------------------------------------------------------------------------- s00 title
class S00Title(TitleCard):
    LESSON = "Scientist profile"
    TITLE = NAME

    def construct(self):
        img, frame = portrait_pair(4.7)
        grp = Group(img, frame)
        grp.move_to([-3.3, 0.35, 0])
        cap = caption_under(frame, size=24).shift(DOWN * 0.15)
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


# ----------------------------------------------------------------------------- s01 the lumber merchant's son
class S01Origin(ProfileScene):
    def construct(self):
        self.add_inset()
        son = lab("a lumber merchant's son", TEXT, 30).move_to([PX, 2.7, 0])
        self.at("lumber")
        self.play(pop(son), run_time=0.5)

        dull = lab("written off: too dull for business", RED, 28).move_to([PX, 1.35, 0])
        a1 = Arrow(son.get_bottom(), dull.get_top(), color=GREY, stroke_width=4, buff=0.08,
                   max_tip_length_to_length_ratio=0.35)
        self.at("written off")
        self.play(GrowArrow(a1), pop(dull), run_time=0.6)

        best = lab(["the most exacting", "organic chemist"], GOLD, 32).move_to([PX - 1.2, -0.45, 0])
        a2 = Arrow([best.get_center()[0], dull.get_bottom()[1], 0], best.get_top() + UP * 0.02, color=GREY, stroke_width=4,
                   buff=0.08, max_tip_length_to_length_ratio=0.35)
        strike = Line(dull.get_left() + RIGHT * 0.3, dull.get_right() - RIGHT * 0.3, color=TEXT, stroke_width=4)
        self.at("Fisher became")
        self.play(Create(strike), dull[0].animate.set_stroke(opacity=0.45), dull[1].animate.set_opacity(0.55), run_time=0.45)
        self.play(GrowArrow(a2), run_time=0.35)
        self.at("most exacting")
        self.play(pop(best), run_time=0.5)

        germany = lab("Germany", PLACE, 30).move_to([PX + 3.3, -0.45, 0])
        self.at("in Germany")
        self.play(pop(germany), run_time=0.45)

        structure = lab("structure", TEAL, 34).move_to([PX + 2.5, -2.3, 0])
        behavior = lab("behavior", ORANGE, 34).move_to([PX - 1.5, -2.3, 0])
        arr = Arrow(behavior.get_right() + RIGHT * 0.1, structure.get_left() + LEFT * 0.1, color=TEAL, stroke_width=5,
                    buff=0, max_tip_length_to_length_ratio=0.3)
        self.at("reading structure")
        self.play(pop(structure), run_time=0.5)
        self.at("off behavior")
        self.play(pop(behavior), GrowArrow(arr), run_time=0.7)
        lbl = T("read off", 24, GREY).next_to(arr, DOWN, buff=0.12)
        self.play(FadeIn(lbl), run_time=0.3)
        self.finish()


# ----------------------------------------------------------------------------- s02 ordering the sugars
class S02Sugars(ProfileScene):
    def construct(self):
        self.add_inset()
        # decade bands
        ay = 2.85
        b80 = Rectangle(width=4.1, height=0.62, stroke_width=0, fill_color=YELLOW, fill_opacity=0.22)
        b90 = b80.copy()
        b80.move_to([-0.3, ay, 0]); b90.move_to([3.9, ay, 0])
        l80 = M("1880s", 32, YELLOW).move_to(b80)
        l90 = M("1890s", 32, YELLOW).move_to(b90)
        self.at("1880s")
        self.play(GrowFromEdge(b80, LEFT), FadeIn(l80), run_time=0.6)
        self.at("1890s")
        self.play(GrowFromEdge(b90, LEFT), FadeIn(l90), run_time=0.6)

        # the sugars: five plain tiles, jumbled, then put in order
        rng = np.random.default_rng(3)
        xs = [-0.6 + 1.3 * i for i in range(5)]
        tiles = VGroup(*[RoundedRectangle(corner_radius=0.1, width=0.8, height=0.8, stroke_color=GREEN, stroke_width=3,
                                          fill_color=GREEN, fill_opacity=0.25) for _ in range(5)])
        jumbled = []
        for t, x, dy, ang in zip(tiles, xs, [0.3, -0.15, 0.25, -0.2, 0.15], [0.7, -0.5, 1.1, -0.9, 0.4]):
            t.move_to([x, 1.3 + dy, 0]).rotate(ang)
        s_lab = T("the sugars", 28, GREEN).move_to([PX - 0.2, 0.3, 0])
        self.at("wrestled")
        self.play(LaggedStart(*[FadeIn(t, scale=0.6) for t in tiles], lag_ratio=0.15), FadeIn(s_lab), run_time=0.8)
        self.at("into order")
        self.play(*[t.animate.rotate(-ang).move_to([x, 1.3, 0]) for t, x, ang in
                    zip(tiles, xs, [0.7, -0.5, 1.1, -0.9, 0.4])], run_time=0.9)

        # the three methods
        osa = lab("osazones", ORANGE, 26)
        oxi = lab("oxidation", ORANGE, 26)
        cya = lab(["cyanohydrin", "chain-extension"], ORANGE, 26)
        tools = VGroup(osa, oxi, cya).arrange(RIGHT, buff=0.3).move_to([PX - 0.05, -1.0, 0])
        self.at("ossizones")
        self.play(pop(osa), Indicate(tiles, color=ORANGE, scale_factor=1.04), run_time=0.6)
        self.at("oxidation")
        self.play(pop(oxi), Indicate(tiles, color=ORANGE, scale_factor=1.04), run_time=0.6)
        self.at("cyanohydrin")
        self.play(pop(cya), Indicate(tiles, color=ORANGE, scale_factor=1.04), run_time=0.8)

        # deducing which hydroxyl pointed which way
        self.at("deducing", lead=0.45)
        self.play(FadeOut(VGroup(tools, tiles, s_lab, b80, b90, l80, l90)), run_time=0.45)
        q = lab(["which hydroxyl", "pointed which way"], TEAL, 32).move_to([PX, 1.6, 0])
        self.play(pop(q), run_time=0.5)
        self.at("pointed which")
        aL = Arrow(q.get_left() + LEFT * 0.1, q.get_left() + LEFT * 1.3, color=TEAL, stroke_width=5, buff=0,
                   max_tip_length_to_length_ratio=0.3)
        aR = Arrow(q.get_right() + RIGHT * 0.1, q.get_right() + RIGHT * 1.3, color=TEAL, stroke_width=5, buff=0,
                   max_tip_length_to_length_ratio=0.3)
        self.play(GrowArrow(aL), GrowArrow(aR), run_time=0.6)

        # long before any instrument could see a molecule
        self.at("long before")
        inst = lab("any instrument", GREY, 30).move_to([PX - 2.2, -1.3, 0])
        mol = lab("a molecule", GREY, 30, fill=0.0).move_to([PX + 2.6, -1.3, 0])
        mol_f = VGroup(DashedVMobject(mol[0], num_dashes=34).set_color(GREY), mol[1])
        self.at("instrument")
        self.play(pop(inst), run_time=0.5)
        look = DashedLine(inst.get_right() + RIGHT * 0.1, mol_f.get_left() + LEFT * 0.1, color=RED, stroke_width=4,
                          dash_length=0.12)
        self.at("could see")
        self.play(Create(look), run_time=0.45)
        cant = T("could not yet see", 28, RED).next_to(look, DOWN, buff=0.7)
        self.play(FadeIn(cross_at(look.get_center(), 0.2)), FadeIn(cant, shift=UP * 0.1), run_time=0.3)
        self.at("a molecule")
        self.play(pop(mol_f), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s03 the projection
def box3d(size=1.3, off=0.45, color=TEAL):
    """An empty wireframe box: the generic stand-in for 'three-dimensional'."""
    s = size
    front = Square(s, stroke_color=color, stroke_width=4)
    back = Square(s, stroke_color=color, stroke_width=4).shift(UR * off)
    links = VGroup(*[Line(front.get_corner(c), back.get_corner(c), color=color, stroke_width=4)
                     for c in (UL, UR, DR)])
    return VGroup(back, links, front)


class S03Projection(ProfileScene):
    def construct(self):
        self.add_inset()
        proj = lab("Fischer projection", GOLD, 36).move_to([PX, 2.75, 0])
        self.at("Fisher projection")
        self.play(pop(proj), run_time=0.55)
        draw = T("you will draw it in this chapter", 28, GREY).move_to([PX, 1.95, 0])
        self.at("you will draw")
        self.play(FadeIn(draw, shift=UP * 0.1), run_time=0.5)
        inv = T("the notation he invented", 28, GOLD).move_to([PX, 1.95, 0])
        self.at("notation")
        self.play(ReplacementTransform(draw, inv), run_time=0.6)

        cube = box3d().move_to([PX - 2.3, 0.35, 0])
        cube_lab = VGroup(T("three-dimensional", 26, TEAL), T("bookkeeping", 26, TEAL)).arrange(DOWN, buff=0.08) \
            .move_to([PX - 2.3, -1.1, 0])
        self.at("three")
        self.play(Create(cube), run_time=0.7)
        self.at("bookkeeping")
        self.play(FadeIn(cube_lab, shift=UP * 0.1), run_time=0.5)

        paper = Rectangle(width=1.7, height=2.1, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.1) \
            .move_to([PX + 2.4, 0.35, 0])
        paper_lab = T("flat paper", 26, TEXT).move_to([PX + 2.4, -1.1, 0])
        arr = Arrow(cube.get_right() + RIGHT * 0.45, paper.get_left() + LEFT * 0.2, color=GOLD, stroke_width=6, buff=0,
                    max_tip_length_to_length_ratio=0.25)
        self.at("straight")
        self.play(GrowArrow(arr), run_time=0.5)
        self.at("flat")
        self.play(FadeIn(paper, scale=0.9), FadeIn(paper_lab), run_time=0.6)

        d = T("D", 76, GOLD, font=TITLE_FONT)
        sl = T("/", 76, GREY, font=TITLE_FONT)
        l = T("L", 76, GOLD, font=TITLE_FONT)
        dl = VGroup(d, sl, l).arrange(RIGHT, buff=0.25).move_to([PX - 1.1, -2.35, 0])
        self.at("D")
        self.play(FadeIn(d, shift=UP * 0.1), run_time=0.3)
        self.play(FadeIn(sl), FadeIn(l, shift=UP * 0.1), run_time=0.35)
        conv = T("convention", 34, GOLD).next_to(dl, RIGHT, buff=0.5).align_to(dl, DOWN).shift(UP * 0.12)
        self.at("convention")
        self.play(FadeIn(conv, shift=RIGHT * 0.1), run_time=0.4)
        self.at("his")
        box = SurroundingRectangle(VGroup(dl, conv), color=GOLD, buff=0.2, stroke_width=3, corner_radius=0.15)
        self.play(Create(box), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s04 lock and key
PROT_PTS = [(-1.7, -0.75), (1.7, -0.75), (1.7, 0.75), (0.5, 0.75), (0.5, 0.05), (-0.5, 0.05), (-0.5, 0.75), (-1.7, 0.75)]
KEY_PTS = [(-0.47, 0.0), (0.47, 0.0), (0.47, 0.7), (1.1, 0.7), (1.1, 1.4), (-1.1, 1.4), (-1.1, 0.7), (-0.47, 0.7)]


def poly(pts, color, fill=0.22):
    return Polygon(*[[x, y, 0] for x, y in pts], stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=fill)


class S04Lockkey(ProfileScene):
    def construct(self):
        self.add_inset()
        title = T("“lock and key”", 40, GOLD, font=TITLE_FONT)
        spec = lab("enzyme specificity", BLUE, 28)
        row = VGroup(title, spec).arrange(RIGHT, buff=0.55).move_to([PX, 2.85, 0])
        self.at("lock and key")
        self.play(FadeIn(title, shift=UP * 0.1), run_time=0.5)
        self.at("enzyme specificity")
        self.play(pop(spec), run_time=0.5)

        cy = -0.6
        prot = poly(PROT_PTS, BLUE, 0.2).move_to([PX, cy, 0])
        prot_lab = T("protein", 30, BLUE).move_to([PX, cy - 0.35, 0])
        key = poly(KEY_PTS, GREEN, 0.3)
        key_lab = T("sugar", 30, GREEN)
        key.move_to([PX, cy + 0.05 + 0.7, 0])      # tab bottom (local y=0) lands on the notch floor
        key.shift(UP * 1.2)
        key_lab.move_to(key.get_center() + UP * 0.35)
        key_grp = VGroup(key, key_lab)
        self.at("a protein")
        self.play(FadeIn(prot, shift=UP * 0.1), FadeIn(prot_lab), run_time=0.6)
        self.at("its sugar")
        self.play(FadeIn(key_grp, shift=DOWN * 0.1), run_time=0.6)
        geo = T("fit together geometrically", 28, GOLD).move_to([PX, cy - 1.35, 0])
        self.at("fit")
        self.play(key_grp.animate.shift(DOWN * 1.2), FadeIn(geo, shift=UP * 0.1), run_time=1.0, rate_func=smooth)
        fit_line = VGroup(*[Line(p, q, color=GOLD, stroke_width=7) for p, q in [
            ([PX - 0.5, cy + 0.05, 0], [PX + 0.5, cy + 0.05, 0]),
            ([PX - 0.5, cy + 0.05, 0], [PX - 0.5, cy + 0.75, 0]),
            ([PX + 0.5, cy + 0.05, 0], [PX + 0.5, cy + 0.75, 0])]])
        self.at("geometrically")
        self.play(Create(fit_line), Indicate(geo, color=GOLD, scale_factor=1.06), run_time=0.6)

        # exactly the principle the lectins run on
        self.at("exactly", lead=0.5)
        assembly = Group(prot, prot_lab, key_grp, fit_line)
        self.play(FadeOut(geo), assembly.animate.scale(0.82).move_to([PX - 2.35, cy + 0.15, 0]), run_time=0.7)
        lectin = lab("lectins", BLUE, 34).move_to([PX + 2.8, cy + 0.15, 0])
        arr = Arrow([PX - 0.6, cy + 0.15, 0], lectin.get_left() + LEFT * 0.12, color=GOLD, stroke_width=6, buff=0,
                    max_tip_length_to_length_ratio=0.25)
        same = T("same principle", 26, GOLD).next_to(arr, UP, buff=0.12)
        self.at("principle")
        self.play(GrowArrow(arr), FadeIn(same), run_time=0.6)
        self.at("lectins")
        self.play(pop(lectin), run_time=0.5)
        end = T("end of this lesson", 26, GREY).next_to(lectin, DOWN, buff=0.3)
        self.at("end of this")
        self.play(FadeIn(end, shift=UP * 0.1), run_time=0.4)
        self.finish()


# ----------------------------------------------------------------------------- s05 the poison
class S05Poison(ProfileScene):
    def construct(self):
        self.add_inset()
        reagent = lab("phenylhydrazine", ORANGE, 32).move_to([PX - 1.9, 0.4, 0])
        self.at("phenylhydrazine")
        self.play(pop(reagent), run_time=0.55)

        fp = lab("fingerprint the sugars", GREEN, 28).move_to([PX + 2.0, 1.9, 0])
        a1 = Arrow(reagent.get_top() + RIGHT * 0.9, fp.get_left() + LEFT * 0.1, color=GREEN, stroke_width=5, buff=0.05,
                   max_tip_length_to_length_ratio=0.25)
        self.at("fingerprint")
        self.play(GrowArrow(a1), pop(fp), run_time=0.7)

        poisoned = lab("poisoned him", RED, 32).move_to([PX + 2.0, -1.2, 0])
        a2 = Arrow(reagent.get_bottom() + RIGHT * 0.9, poisoned.get_left() + LEFT * 0.1, color=RED, stroke_width=5,
                   buff=0.05, max_tip_length_to_length_ratio=0.25)
        self.at("also")
        self.play(GrowArrow(a2), run_time=0.5)
        slow = T("slowly", 30, RED, font=TITLE_FONT).next_to(a2.get_center(), DOWN, buff=0.3).shift(LEFT * 0.85)
        self.at("slowly")
        track = Rectangle(width=4.2, height=0.22, stroke_color=RED, stroke_width=2, fill_opacity=0) \
            .move_to([PX + 2.0, -2.15, 0])
        bar = Rectangle(width=0.01, height=0.22, stroke_width=0, fill_color=RED, fill_opacity=0.9) \
            .move_to(track.get_left() + RIGHT * 0.005)
        self.play(FadeIn(slow, shift=UP * 0.1), FadeIn(track), run_time=0.3)
        self.add(bar)
        self.play(bar.animate.stretch_to_fit_width(4.2, about_edge=LEFT).align_to(track, LEFT),
                  Succession(Wait(0.6), pop(poisoned)), run_time=1.4, rate_func=linear)

        # he died in 1919
        self.at("He died", lead=0.5)
        self.play(FadeOut(VGroup(reagent, fp, a1, a2, slow, poisoned, track, bar)), run_time=0.4)
        died = T("he died in", 38, TEXT, font=TITLE_FONT).move_to([PX, 1.0, 0])
        yr = M("1919", 96, YELLOW).move_to([PX, -0.4, 0])
        self.play(FadeIn(died, shift=UP * 0.1), run_time=0.4)
        self.at("1919")
        self.play(Write(yr), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- s06 the quote
class S06Quote(ProfileScene):
    def construct(self):
        self.add_inset()
        lines = ["“Enzyme and glucoside must fit", "together like a lock and key.”"]
        q = VGroup(*[T(l, 40, TEXT, font=TITLE_FONT) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        fit(q, max_w=8.4)
        who = T("— Emil Fischer", 32, GOLD)
        g = VGroup(q, who).arrange(DOWN, aligned_edge=RIGHT, buff=0.6).move_to([PX, 0.3, 0])
        for ln in q:
            ln.set_opacity(0)
        who.set_opacity(0)
        self.add(g)
        self.wait(0.4)
        for ln in q:
            self.play(ln.animate.set_opacity(1.0), run_time=0.9)
        self.wait(0.6)
        self.play(who.animate.set_opacity(1.0), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s07 end card
class S07End(NarratedScene):
    LINE = "Deduced sugar configurations, invented the Fischer projection, and pictured lock-and-key recognition."

    def construct(self):
        img, frame = portrait_pair(2.3)
        img.move_to([0, 2.0, 0]); frame.move_to([0, 2.0, 0])
        cap = T(CAPTION, 22, GREY).move_to([0, 2.0 - 1.15 - 0.3, 0])
        a = T("Deduced sugar configurations, invented the Fischer", 38, font=TITLE_FONT)
        b = T("projection, and pictured lock-and-key recognition.", 38, font=TITLE_FONT)
        lg = VGroup(a, b).arrange(DOWN, buff=0.2).move_to([0, -0.55, 0])
        fit(lg, max_w=11.5)
        sub = T("biochemistrypedia.com", 24, TEAL).move_to([0, -1.85, 0])
        src = T("Source: The Molecule Hunters (v10) · Emil Fischer profile", 22, GREY).move_to([0, -2.6, 0])
        self.play(FadeIn(img), FadeIn(frame), FadeIn(cap), run_time=0.5)
        self.play(FadeIn(lg, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(sub), FadeIn(src), run_time=0.4)
        self.finish()
