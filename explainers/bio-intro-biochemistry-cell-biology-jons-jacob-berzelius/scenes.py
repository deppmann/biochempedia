"""Jöns Jacob Berzelius: a scientist profile (Biochemistrypedia, intro-biochemistry-cell-biology lesson).

Narration is the lesson entry's `story`, verbatim. Everything on screen comes from that entry
(name, dates, contribution, story, quotes). The portrait is an AI-generated engraving-style
illustration from The Molecule Hunters; it is captioned "illustration · AI-generated" whenever it is
on screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = Berzelius: his name/dates, portrait frame, "empire of measurement", the standard he set
  GREY   = the old way (pictograms), structure, labels
  GREEN  = the new chemical signs (letters H, O, Fe) and the "again, done right" redo
  PLACE (lavender) = places: the converted kitchen, Stockholm
  BLUE   = atomic weights and the 45 elements
  AMBER  = sand
  RED    = heat, and what failed: rushed, badly done, swept aside, speed without care
  TEAL   = the words he coined: protein, catalysis
  YELLOW = Wöhler's first analysis (the sheet)
No molecular structure is drawn: pictograms are loose circles / crescents / strokes, the apparatus is
a schematic flask on a tray, the elements are plain tiles.
"""
import math
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

PORTRAIT = str(Path(__file__).resolve().parent / "berz.png")
NAME = "Jöns Jacob Berzelius"
DATES = "1779–1848"
CAPTION = "illustration · AI-generated"
PLACE = "#B39DDB"
AMBER = "#E0A458"

INSET_C = np.array([-4.6, 1.3, 0.0])
INSET_H = 3.4
CX = 1.95   # x center of the right panel (x from -2.4 to 6.3)


# ----------------------------------------------------------------------------- helpers
def portrait_pair(height):
    img = ImageMobject(PORTRAIT).set_height(height)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["cubic"])
    frame = Rectangle(width=img.width, height=img.height, stroke_color=GOLD, stroke_width=3, fill_opacity=0)
    return img, frame


def inset_group():
    img, frame = portrait_pair(INSET_H)
    img.move_to(INSET_C)
    frame.move_to(INSET_C)
    cap = T(CAPTION, 22, GREY, font=TITLE_FONT).next_to(frame, DOWN, buff=0.2)
    nm = T(NAME, 28, font=TITLE_FONT)
    dt = T(DATES, 26, GOLD)
    tag = VGroup(nm, dt).arrange(DOWN, buff=0.12).move_to([INSET_C[0], INSET_C[1] - INSET_H / 2 - 1.2, 0])
    rule = Line([-2.55, -3.2, 0], [-2.55, 3.2, 0], color=GREY, stroke_width=1.5).set_opacity(0.35)
    return img, frame, cap, tag, rule


def lab(text, color=BLUE, size=28, pad=0.22, fill=0.16):
    return chip(text, color, size, pad, fill)


def pop(mob, d=UP):
    return FadeIn(mob, shift=d * 0.12)


def crescent(r, color, angle=0.0):
    c = Difference(Circle(radius=r), Circle(radius=r * 0.86).shift(RIGHT * 0.5 * r),
                   stroke_color=color, stroke_width=3.5, fill_opacity=0)
    return c.rotate(angle)


def ring_dot(r, color):
    return VGroup(Circle(radius=r, color=color, stroke_width=3.5), Dot(radius=r * 0.22, color=color))


def zig(color, w=0.7, h=0.3):
    m = VMobject(color=color, stroke_width=3.5)
    m.set_points_as_corners([[-w / 2, -h / 2, 0], [-w / 6, h / 2, 0], [w / 6, -h / 2, 0], [w / 2, h / 2, 0]])
    return m


def cross(color, s=0.5):
    return VGroup(Line([-s / 2, 0, 0], [s / 2, 0, 0], color=color, stroke_width=3.5),
                  Line([0, -s / 2, 0], [0, s / 2, 0], color=color, stroke_width=3.5))


def tri(color, s=0.55):
    return Polygon([-s / 2, -s / 2.4, 0], [s / 2, -s / 2.4, 0], [0, s / 2, 0], color=color, stroke_width=3.5)


def clutter(color=GREY):
    """Three loose clusters of old pictograms: circles / crescents / fragments (not molecules: no bonds)."""
    circ = VGroup(Circle(radius=0.34, color=color, stroke_width=3.5).shift([-0.55, 0.3, 0]),
                  ring_dot(0.24, color).shift([0.4, -0.1, 0]),
                  Circle(radius=0.16, color=color, stroke_width=3.5).shift([-0.15, -0.55, 0]))
    cres = VGroup(crescent(0.38, color, 0.5).shift([-0.5, 0.2, 0]),
                  crescent(0.3, color, -2.2).shift([0.35, 0.45, 0]),
                  crescent(0.34, color, 3.4).shift([0.05, -0.5, 0]))
    frag = VGroup(zig(color).shift([-0.2, 0.45, 0]), cross(color).rotate(0.4).shift([0.55, -0.1, 0]),
                  tri(color).rotate(-0.3).shift([-0.5, -0.4, 0]), zig(color, 0.5, 0.25).rotate(1.2).shift([0.35, 0.6, 0]))
    return circ, cres, frag


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
        cap = T(CAPTION, 24, GREY, font=TITLE_FONT).next_to(frame, DOWN, buff=0.2).shift(DOWN * 0.15)
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        name = T(self.TITLE, size=52, font=TITLE_FONT)
        fit(name, max_w=7.6)
        dates = T(DATES, size=38, color=GOLD)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        txt = VGroup(brand, lesson, name, dates, rule).arrange(DOWN, buff=0.3).move_to([3.3, 0.2, 0])
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


# ----------------------------------------------------------------------------- s01 the clutter
BOX_C = np.array([CX, -0.25, 0.0])


def old_box():
    box = DashedVMobject(RoundedRectangle(corner_radius=0.25, width=8.6, height=3.1, stroke_color=GREY, stroke_width=3),
                         num_dashes=72, dashed_ratio=0.6)
    box.move_to(BOX_C)
    circ, cres, frag = clutter()
    for g, x in zip((circ, cres, frag), (-2.85, -0.1, 2.5)):
        g.scale(1.3).move_to(BOX_C + np.array([x, 0.35, 0]))
    labs = [T("circles", 24, GREY).move_to([circ.get_center()[0], BOX_C[1] - 1.2, 0]),
            T("crescents", 24, GREY).move_to([cres.get_center()[0], BOX_C[1] - 1.2, 0]),
            T("fragments of alchemy", 24, GREY).move_to([frag.get_center()[0], BOX_C[1] - 1.2, 0])]
    return box, (circ, cres, frag), labs


class S01Pictograms(ProfileScene):
    def construct(self):
        self.add_inset()
        box, groups, labs = old_box()
        title = T("Before Berzelius", 36, GREY, font=TITLE_FONT).move_to([CX, 3.0, 0])
        self.at("Before him")
        self.play(FadeIn(title, shift=UP * 0.1), run_time=0.5)
        comp = lab("a compound", GREY, 28).move_to([CX, 2.0, 0])
        self.at("drew compounds")
        self.play(pop(comp), run_time=0.45)
        self.at("clutter")
        arr = Arrow([CX, 1.62, 0], [CX, 1.38, 0], buff=0, color=GREY, stroke_width=4, max_tip_length_to_length_ratio=0.8)
        self.play(Create(box), GrowArrow(arr), run_time=0.8)
        pic = T("little pictograms", 28, GREY).move_to([CX, -2.3, 0])
        self.at("pictograms")
        self.play(FadeIn(pic, shift=UP * 0.1), run_time=0.4)
        for g, l, ph in zip(groups, labs, ("circles", "crescents", "fragments of alchemy")):
            self.at(ph)
            self.play(LaggedStart(*[FadeIn(m, scale=0.5) for m in g], lag_ratio=0.25), FadeIn(l), run_time=0.8)
        self.wait(0.3)
        self.finish()


# ----------------------------------------------------------------------------- s02 letters
def beam_group(tilt):
    """Schematic balance: beam on a pivot, two pans. tilt in radians."""
    piv = Triangle(color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.35).scale(0.3)
    base = Line([-0.5, 0, 0], [0.5, 0, 0], color=GREY, stroke_width=4)
    beam = Line([-2.2, 0, 0], [2.2, 0, 0], color=GREY, stroke_width=6).rotate(tilt)
    return piv, base, beam


class S02Letters(ProfileScene):
    def construct(self):
        self.add_inset()
        box, groups, labs = old_box()
        allold = VGroup(box, *groups)
        self.add(allold, *labs)
        self.at("proposed", lead=0.3)
        head = T("Berzelius's proposal", 34, GOLD, font=TITLE_FONT).move_to([CX, 3.0, 0])
        self.play(FadeOut(VGroup(*labs)), run_time=0.25)
        self.play(allold.animate.scale(0.34).move_to([CX - 2.3, 1.85, 0]).set_opacity(0.5),
                  FadeIn(head, shift=UP * 0.1), run_time=0.7)
        old_lab = T("pictograms", 24, GREY).next_to(allold, DOWN, buff=0.15).set_opacity(0.7)
        self.play(FadeIn(old_lab), run_time=0.3)
        self.at("insultingly simple")
        simple = VGroup(T("almost", 28, GOLD), T("insultingly simple", 28, GOLD)).arrange(DOWN, buff=0.08).move_to([4.6, 1.85, 0])
        self.play(FadeIn(simple, shift=LEFT * 0.15), run_time=0.5)

        self.at("the chemical signs ought")
        q1 = T("“The chemical signs ought to be", 34, GREEN, font=TITLE_FONT)
        q1b = T("letters …”", 34, GREEN, font=TITLE_FONT)
        qg = VGroup(q1, q1b).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([CX + 0.3, 0.05, 0])
        self.play(FadeOut(simple), Write(q1, run_time=1.3))
        self.at("letters")
        self.play(Write(q1b, run_time=0.6))
        letters = VGroup(M("H", 64, GREEN), M("O", 64, GREEN), M("Fe", 64, GREEN)).arrange(RIGHT, buff=0.9).move_to([CX + 0.3, -1.55, 0])
        self.play(LaggedStart(*[FadeIn(l, scale=0.6) for l in letters], lag_ratio=0.3), run_time=0.9)

        self.at("for the chemical sign", lead=0.3)
        self.play(FadeOut(letters), FadeOut(qg), run_time=0.3)
        name = lab("Latin name", GREY, 30).move_to([-0.3, -0.1, 0])
        sign = lab("chemical sign", GREEN, 30).move_to([4.5, -0.1, 0])
        a = Arrow(name.get_right() + RIGHT * 0.08, sign.get_left() + LEFT * 0.08, buff=0, color=GREEN, stroke_width=5,
                  max_tip_length_to_length_ratio=0.2)
        init = T("initial letter", 28, GREEN).next_to(a, UP, buff=0.18)
        self.play(pop(name), run_time=0.4)
        self.at("initial letter of the latin name", lead=0.3)
        self.play(GrowArrow(a), FadeIn(init), run_time=0.5)
        self.play(pop(sign), run_time=0.4)

        self.at("fe for iron", lead=0.35)
        self.play(FadeOut(VGroup(name, sign, a, init)), run_time=0.35)
        fe = M("Fe", 96, GREEN).move_to([-0.3, -0.1, 0])
        eq = M("=", 60, GREY).move_to([1.5, -0.1, 0])
        iron = T("iron", 56, GREY, font=TITLE_FONT).move_to([3.4, -0.1, 0])
        self.play(Write(fe), run_time=0.5)
        self.at("iron")
        self.play(FadeIn(eq), FadeIn(iron, shift=LEFT * 0.2), run_time=0.5)

        self.at("balance an equation", lead=0.3)
        self.play(FadeOut(VGroup(fe, eq, iron)), run_time=0.3)
        by = -0.25
        piv, base, beam = beam_group(0.22)
        piv.move_to([CX, by - 0.5, 0]); base.move_to([CX, by - 0.92, 0])
        # beam as a tracker-driven line, tilted then levelled
        tr = ValueTracker(0.22)
        c = np.array([CX, by, 0])
        def mk_beam():
            ang = tr.get_value()
            d = np.array([math.cos(ang), math.sin(ang), 0])
            l = Line(c - 2.2 * d, c + 2.2 * d, color=GREY, stroke_width=6)
            return l
        def mk_pans():
            ang = tr.get_value()
            d = np.array([math.cos(ang), math.sin(ang), 0])
            out = VGroup()
            for s in (-1, 1):
                e = c + s * 2.2 * d
                out.add(Line(e, e + DOWN * 0.5 + LEFT * 0.55 * 1, color=GREY, stroke_width=3),
                        Line(e, e + DOWN * 0.5 + RIGHT * 0.55, color=GREY, stroke_width=3),
                        Line(e + DOWN * 0.5 + LEFT * 0.55, e + DOWN * 0.5 + RIGHT * 0.55, color=GREY, stroke_width=5))
            return out
        beam_m = always_redraw(mk_beam)
        pans_m = always_redraw(mk_pans)
        bal_lab = T("balance an equation", 30, GREY).move_to([3.3, 1.25, 0])
        piv2 = Line([CX, by, 0], [CX, by - 0.9, 0], color=GREY, stroke_width=5)
        self.add(beam_m, pans_m)
        self.play(FadeIn(bal_lab), Create(piv2), Create(base.move_to([CX, by - 0.9, 0])), run_time=0.5)
        self.play(tr.animate.set_value(-0.12), run_time=0.6)
        self.play(tr.animate.set_value(0.0), run_time=0.5)

        self.at("grammar", lead=0.4)
        self.play(FadeOut(VGroup(beam_m, pans_m, piv2, base, bal_lab)), run_time=0.25)
        page = RoundedRectangle(corner_radius=0.12, width=6.4, height=2.2, stroke_color=GREY, stroke_width=3,
                                fill_color=GREY, fill_opacity=0.1).move_to([CX, -0.35, 0])
        row = VGroup(M("H", 64, GREEN), M("O", 64, GREEN), M("Fe", 64, GREEN)).arrange(RIGHT, buff=0.9).move_to(page)
        gram = T("the grammar he laid on the page", 30, GOLD, font=TITLE_FONT).move_to([CX, -2.0, 0])
        self.play(Create(page), LaggedStart(*[FadeIn(l, scale=0.6) for l in row], lag_ratio=0.25), run_time=0.6)
        self.at("laid on the page")
        self.play(FadeIn(gram, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s03 the kitchen
def flask(color=GREY, fill=BLUE):
    body = Circle(radius=0.55, stroke_color=color, stroke_width=4)
    neck = Rectangle(width=0.36, height=0.6, stroke_color=color, stroke_width=4).move_to([0, 0.75, 0])
    liquid = Circle(radius=0.55, stroke_width=0, fill_color=fill, fill_opacity=0.5).scale(0.85).shift(DOWN * 0.1)
    return VGroup(liquid, body, neck)


def wavy(x0, x1, y, amp=0.09, n=3, color=RED):
    return ParametricFunction(lambda t: np.array([t, y + amp * math.sin((t - x0) * 2 * PI * n / (x1 - x0)), 0]),
                              t_range=[x0, x1], color=color, stroke_width=4)


class S03Kitchen(ProfileScene):
    def construct(self):
        self.add_inset()
        head = T("empire of measurement", 34, GOLD, font=TITLE_FONT).move_to([CX, 3.0, 0])
        self.at("empire of measurement")
        self.play(Write(head, run_time=1.2))

        room = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=7.8, height=3.5, stroke_color=PLACE, stroke_width=4),
                              num_dashes=64, dashed_ratio=0.65).move_to([CX, 0.9, 0])
        kit = T("converted kitchen", 28, PLACE).move_to([CX - 2.2, -1.5, 0])
        self.at("converted kitchen")
        self.play(Create(room), FadeIn(kit, shift=UP * 0.1), run_time=0.9)
        self.at("Stockholm")
        st = lab("Stockholm", PLACE, 28).move_to([CX + 2.6, -1.5, 0])
        self.play(pop(st), run_time=0.45)

        fx, fy = CX - 0.9, 1.15
        fl = flask().move_to([fx, fy, 0])
        self.at("heating samples")
        samp = T("samples", 26, BLUE).move_to([fx - 1.9, fy + 0.2, 0])
        self.play(FadeIn(fl, shift=DOWN * 0.15), FadeIn(samp), run_time=0.6)
        heat = VGroup(wavy(fx - 0.7, fx + 0.7, fy - 0.9), wavy(fx - 0.7, fx + 0.7, fy - 1.1))
        tray = Polygon([fx - 1.1, fy - 0.56, 0], [fx + 1.1, fy - 0.56, 0], [fx + 0.8, fy - 0.9, 0], [fx - 0.8, fy - 0.9, 0],
                       stroke_color=AMBER, stroke_width=4, fill_color=AMBER, fill_opacity=0.4)
        rng = np.random.default_rng(3)
        sand = VGroup(*[Dot([fx + rng.uniform(-0.8, 0.8), fy - 0.58 - rng.uniform(0.04, 0.3), 0], radius=0.03, color=AMBER) for _ in range(16)])
        # heat lines sit below the tray
        heat = VGroup(wavy(fx - 0.7, fx + 0.7, fy - 1.15), wavy(fx - 0.7, fx + 0.7, fy - 1.38))
        self.at("domestic sand bath")
        bath = T("domestic sand bath", 26, AMBER).move_to([fx + 3.0, fy - 0.75, 0])
        ptr = Arrow(bath.get_left() + LEFT * 0.08, [fx + 1.15, fy - 0.75, 0], buff=0, color=AMBER, stroke_width=3,
                    max_tip_length_to_length_ratio=0.3)
        self.play(FadeIn(tray, shift=UP * 0.1), FadeIn(sand), FadeIn(bath), GrowArrow(ptr), run_time=0.7)
        self.play(Create(heat), run_time=0.5)
        self.play(heat.animate.shift(UP * 0.06), run_time=0.3)

        # ---- atomic weights of 45 elements
        self.at("from that kitchen", lead=0.15)
        phase1 = Group(room, kit, st, fl, samp, tray, sand, bath, ptr, heat, head)
        mini = lab("the kitchen", PLACE, 24).move_to([-0.3, 3.0, 0])
        self.play(FadeOut(phase1), FadeIn(mini), run_time=0.5)
        self.at("measured the atomic weights")
        aw = T("atomic weights", 32, BLUE).move_to([3.4, 3.0, 0])
        self.play(pop(aw), run_time=0.45)
        tiles = VGroup(*[Square(0.4, stroke_color=BLUE, stroke_width=2.5, fill_color=BLUE, fill_opacity=0.25) for _ in range(45)])
        tiles.arrange_in_grid(5, 9, buff=0.1).move_to([3.3, 1.35, 0])
        n45 = M("45", 80, BLUE).move_to([-0.1, 1.5, 0])
        el = T("elements", 30, BLUE).next_to(n45, DOWN, buff=0.1)
        self.at("45 elements")
        self.play(LaggedStart(*[FadeIn(t, scale=0.4) for t in tiles], lag_ratio=0.03), FadeIn(n45), run_time=1.1)
        self.play(FadeIn(el), run_time=0.3)

        # ---- within a few percent
        self.at("within a few percent", lead=0.15)
        ly = -1.45
        line = Line([-1.4, ly, 0], [6.1, ly, 0], color=GREY, stroke_width=4)
        x_his, x_now = 3.0, 3.5
        t_his = Line([x_his, ly - 0.3, 0], [x_his, ly + 0.3, 0], color=BLUE, stroke_width=6)
        t_now = Line([x_now, ly - 0.3, 0], [x_now, ly + 0.3, 0], color=TEXT, stroke_width=6)
        l_his = T("his value", 26, BLUE).move_to([x_his - 1.0, ly + 0.75, 0])
        l_now = T("today's value", 26, TEXT).move_to([x_now + 1.2, ly + 0.75, 0])
        s1 = Line([x_his - 0.1, ly + 0.45, 0], [x_his - 0.02, ly + 0.35, 0], color=BLUE, stroke_width=3)
        s2 = Line([x_now + 0.1, ly + 0.45, 0], [x_now + 0.02, ly + 0.35, 0], color=TEXT, stroke_width=3)
        self.play(Create(line), FadeIn(t_his), FadeIn(l_his), run_time=0.6)
        self.at("the values we use today", lead=0.3)
        self.play(FadeIn(t_now), FadeIn(l_now), run_time=0.5)
        br = BraceBetweenPoints([x_his - 0.05, ly - 0.38, 0], [x_now + 0.05, ly - 0.38, 0], direction=DOWN, color=BLUE)
        few = T("within a few percent", 28, BLUE).next_to(br, DOWN, buff=0.15)
        self.play(GrowFromCenter(br), FadeIn(few), run_time=0.6)

        # ---- coined protein, catalysis
        self.at("coined protein", lead=0.35)
        self.play(FadeOut(Group(mini, aw, tiles, n45, el, line, t_his, t_now, l_his, l_now, br, few)), run_time=0.4)
        coined = T("He also coined", 32, GOLD, font=TITLE_FONT).move_to([CX, 2.2, 0])
        self.play(pop(coined), run_time=0.4)
        prot = lab("protein", TEAL, 44, pad=0.3).move_to([CX - 1.7, 0.7, 0])
        cat = lab("catalysis", TEAL, 44, pad=0.3).move_to([CX + 2.0, 0.7, 0])
        self.at("protein")
        self.play(pop(prot), run_time=0.45)
        self.at("catalysis")
        self.play(pop(cat), run_time=0.45)
        self.at("two words")
        w = T("two words this course cannot do without", 30, GREY).move_to([CX, -1.0, 0])
        self.play(FadeIn(w, shift=UP * 0.1), run_time=0.5)
        self.play(Indicate(prot, color=GOLD, scale_factor=1.06), Indicate(cat, color=GOLD, scale_factor=1.06), run_time=0.9)
        self.finish()


# ----------------------------------------------------------------------------- s04 exacting
class S04Exacting(ProfileScene):
    def construct(self):
        self.add_inset()
        self.at("exacting")
        ex = T("exacting", 44, GOLD, font=TITLE_FONT).move_to([CX, 3.0, 0])
        exl = Line([CX - 1.2, 2.62, 0], [CX + 1.2, 2.62, 0], color=GOLD, stroke_width=3)
        self.play(pop(ex), run_time=0.5)
        self.play(GrowFromCenter(exl), run_time=0.6)

        frame = DashedVMobject(RoundedRectangle(corner_radius=0.2, width=8.3, height=3.7, stroke_color=PLACE, stroke_width=3.5),
                               num_dashes=60, dashed_ratio=0.65).move_to([CX, 0.65, 0])
        ktag = T("that kitchen", 26, PLACE).move_to([-0.7, 2.15, 0])

        woh = lab("young Friedrich Wöhler", TEXT, 26).move_to([0.15, 1.1, 0])
        self.at("young Friedrich")
        self.play(pop(woh), run_time=0.45)

        sheet = VGroup(Rectangle(width=1.5, height=1.1, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.12),
                       *[Line([-0.5, 0.3 - 0.25 * i, 0], [0.5 - 0.15 * i, 0.3 - 0.25 * i, 0], color=YELLOW, stroke_width=2.5) for i in range(3)])
        sheet.move_to([-0.2, -0.3, 0])
        speed = VGroup(*[Line([-1.9 - 0.15 * (i % 2), -0.05 - 0.28 * i, 0], [-1.25, -0.05 - 0.28 * i, 0], color=RED, stroke_width=4) for i in range(3)])
        first = T("first analysis", 26, YELLOW).move_to([2.3, -0.1, 0])
        rushed = T("rushed", 26, RED).move_to([2.3, -0.6, 0])
        self.at("rushed")
        self.play(sheet.animate.set_opacity(1).shift(ORIGIN), FadeIn(sheet, shift=RIGHT * 1.5), run_time=0.4)
        self.play(Create(speed), FadeIn(rushed), run_time=0.4)
        self.at("first analysis")
        self.play(FadeIn(first, shift=LEFT * 0.1), run_time=0.4)
        self.at("in that kitchen")
        self.play(Create(frame), FadeIn(ktag), run_time=0.8)

        ber = lab("Berzelius", GOLD, 28).move_to([4.8, 1.1, 0])
        self.at("Berzelius glanced")
        self.play(pop(ber), run_time=0.4)
        gaze = Arrow(ber.get_left() + LEFT * 0.1 + DOWN * 0.15, sheet.get_top() + UP * 0.1 + RIGHT * 0.35, buff=0, color=GOLD, stroke_width=3,
                     max_tip_length_to_length_ratio=0.12)
        glanced = T("glanced", 24, GOLD).move_to([4.3, -0.15, 0]).rotate(0)
        self.at("glanced", lead=0.0)
        self.play(GrowArrow(gaze), run_time=0.3)

        self.at("verdict")
        ver = Arrow(ber.get_left() + LEFT * 0.08, woh.get_right() + RIGHT * 0.08, buff=0, color=RED, stroke_width=5,
                    max_tip_length_to_length_ratio=0.2)
        vl = T("verdict", 28, RED).next_to(ver, UP, buff=0.12)
        self.play(FadeOut(gaze), GrowArrow(ver), FadeIn(vl), run_time=0.5)
        self.at("trailed Wöhler for life")
        life = T("for life", 26, RED).next_to(ver, DOWN, buff=0.15)
        trail = DashedLine(ver.get_start() + DOWN * 0.45, woh.get_bottom() + RIGHT * 0.9 + DOWN * 0.05, color=YELLOW, stroke_width=3)
        self.play(FadeIn(life, shift=UP * 0.1), run_time=0.5)

        self.at("doctor that was quickly")
        quote = T("“Doctor, that was quickly and badly done.”", 34, RED, font=TITLE_FONT)
        fit(quote, max_w=8.4)
        quote.move_to([CX, -2.15, 0])
        self.play(Write(quote, run_time=2.4))

        # swept aside
        self.at("swept aside", lead=0.3)
        sw = Arrow([1.4, -0.3, 0], [3.9, -0.3, 0], buff=0, color=RED, stroke_width=5, max_tip_length_to_length_ratio=0.2).set_opacity(0)
        self.play(sheet.animate.shift(RIGHT * 7).set_opacity(0), FadeOut(speed), FadeOut(rushed), FadeOut(first),
                  run_time=0.8, rate_func=rush_into)
        swept = T("swept aside", 28, RED).move_to([2.3, -0.3, 0])
        self.play(FadeIn(swept), run_time=0.3)
        self.at("to be done again")
        sheet2 = VGroup(Rectangle(width=1.5, height=1.1, stroke_color=GREEN, stroke_width=3, fill_color=GREEN, fill_opacity=0.12),
                        *[Line([-0.5, 0.3 - 0.25 * i, 0], [0.5, 0.3 - 0.25 * i, 0], color=GREEN, stroke_width=2.5) for i in range(3)])
        sheet2.move_to([-0.2, -0.3, 0])
        again = T("done again", 28, GREEN).move_to([2.3, -0.3, 0])
        self.play(FadeOut(swept), FadeIn(sheet2, shift=UP * 0.2), FadeIn(again), run_time=0.7)

        # speed without care
        self.at("Speed without care", lead=0.4)
        self.play(FadeOut(Group(frame, ktag, woh, ber, ver, vl, life, sheet2, again, quote, ex, exl)), run_time=0.4)
        sp = lab("speed", RED, 38, pad=0.26)
        wc = T("without care", 32, GREY)
        eq = M("= nothing", 36, GOLD)
        VGroup(sp, wc, eq).arrange(RIGHT, buff=0.4).move_to([CX, 0.9, 0])
        self.at("Speed without care")
        self.play(pop(sp), run_time=0.4)
        self.play(FadeIn(wc, shift=LEFT * 0.1), run_time=0.4)
        self.at("counted for nothing")
        self.play(FadeIn(eq, shift=LEFT * 0.2), run_time=0.5)

        self.at("The standard", lead=0.5)
        self.play(FadeOut(Group(sp, wc, eq)), run_time=0.3)
        base = Rectangle(width=6.6, height=0.55, stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.3).move_to([CX, -1.6, 0])
        base_l = T("the standard", 30, GOLD, font=TITLE_FONT).move_to(base)
        self.play(GrowFromEdge(base, LEFT), FadeIn(base_l), run_time=0.6)
        self.at("this whole field")
        blocks = VGroup(*[Rectangle(width=1.55, height=0.62, stroke_color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.2)
                          for _ in range(4)])
        blocks.arrange(RIGHT, buff=0.12).move_to([CX, -1.0, 0])
        blocks2 = VGroup(*[b.copy() for b in blocks[:3]]).arrange(RIGHT, buff=0.12).move_to([CX, -0.32, 0])
        field = T("this whole field", 28, BLUE).move_to([CX, 0.6, 0])
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in list(blocks) + list(blocks2)], lag_ratio=0.2), FadeIn(field), run_time=1.0)
        self.finish()


# ----------------------------------------------------------------------------- s05 quote
class S05Quote(ProfileScene):
    def construct(self):
        self.add_inset()
        lines = ["“The chemical signs ought to be", "letters, for the greater facility of", "writing. I shall take, therefore, for",
                 "the chemical sign, the initial letter", "of the Latin name.”"]
        q = VGroup(*[T(l, 36, TEXT, font=TITLE_FONT) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        fit(q, max_w=8.4)
        who = T("— Jöns Jacob Berzelius", 30, GOLD)
        g = VGroup(q, who).arrange(DOWN, aligned_edge=RIGHT, buff=0.5).move_to([CX, 0.1, 0])
        for ln in q:
            ln.set_opacity(0)
        who.set_opacity(0)
        self.add(g)
        self.wait(0.3)
        for ln in q:
            self.play(ln.animate.set_opacity(1.0), run_time=0.6)
        self.wait(0.3)
        self.play(who.animate.set_opacity(1.0), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s06 end card
class S06End(EndCard):
    LINE = "Gave chemistry its alphabet, measured forty-five atomic weights, coined protein and catalysis."

    def construct(self):
        img, frame = portrait_pair(2.3)
        grp = Group(img, frame).move_to([0, 2.05, 0])
        cap = T(CAPTION, 22, GREY).next_to(frame, DOWN, buff=0.15)
        a = T("Gave chemistry its alphabet, measured", size=40, font=TITLE_FONT)
        b = T("forty-five atomic weights, coined protein and catalysis.", size=40, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.2)
        fit(line, max_w=11.8)
        line.move_to([0, -0.75, 0])
        sub = T("biochemistrypedia.com", 24, TEAL).move_to([0, -1.85, 0])
        src = T("Source: The Molecule Hunters (v10) · Berzelius profile", 22, GREY).move_to([0, -2.55, 0])
        self.play(FadeIn(img), FadeIn(frame), FadeIn(cap), run_time=0.5)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(sub), FadeIn(src), run_time=0.4)
        self.finish()
