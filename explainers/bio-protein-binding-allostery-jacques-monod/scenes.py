"""Jacques Monod: a scientist profile (Biochemistrypedia, protein-binding-allostery lesson).

Narration is the lesson entry's `story`, verbatim (split at sentence boundaries). Everything on screen
comes from that entry (name, dates, contribution, story, quotes). The portrait is an AI-generated
engraving-style illustration from The Molecule Hunters (cropped to the face); it is captioned
"illustration · AI-generated" whenever it is on screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = Monod: his name/dates, his portrait frame, time labels (1964, 1965), "allostery" (the word he coined)
  WYMAN  = Jeffries Wyman (periwinkle) (the thermodynamicist, and the proof he held)
  GREEN  = Jean-Pierre Changeux
  PLACE  = places: the lab, the Institut Pasteur, the blackboard
  TEAL   = the protein (hemoglobin) and its relaxed state
  ORANGE = the tense state
  YELLOW = the site that does the work
  PURPLE = the site that controls whether the work can happen
  RED    = acid (and the crossed-out rigid-machine picture)
  PINK   = muscle
  GREY   = structure, bench, de-emphasized things, the missing mechanism
No molecular structure is drawn: proteins are schematic wobbling blobs with two marked patches, the two
states are blobs of different size and color, the balance is a slider.
"""
import math
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

HERE = Path(__file__).resolve().parent
PORTRAIT = str(HERE / "monod_crop.png")
CAPTION = "illustration · AI-generated"
PLACE = "#B39DDB"       # places and institutions
PURPLE = "#B58CD9"      # the control site
ORANGE = "#E8913A"      # the tense state
WYMAN = "#7C9CFF"      # Jeffries Wyman (periwinkle: BLUE is too close to TEAL)
PINK = "#E58AA3"        # muscle
NAME = "Jacques Monod"
DATES = "1910–1976"

INSET_C = np.array([-4.6, 1.15, 0.0])
INSET_H = 3.2
PANEL_C = 1.95          # x center of the right panel (x from -2.4 to 6.3)


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


def dashed(chipmob, color, n=40):
    """Dashed-outline version of a chip: something that is missing."""
    return VGroup(DashedVMobject(chipmob[0], num_dashes=n, dashed_ratio=0.55).set_color(color), chipmob[1])


def pop(mob):
    return FadeIn(mob, shift=UP * 0.12)


def xmark(center, size=0.3, color=RED, width=8):
    return VGroup(Line([-size, -size, 0], [size, size, 0]), Line([-size, size, 0], [size, -size, 0])) \
        .set_color(color).set_stroke(width=width).move_to(center)


def person(label, color, center, r=0.4, size=26, role=None):
    """A person marker (circle + name; optional role line), nothing drawn of a face."""
    dot = Circle(radius=r, color=color, stroke_width=4, fill_color=color, fill_opacity=0.25).move_to(center)
    nm = T(label, size, color, weight=BOLD).next_to(dot, DOWN, buff=0.15)
    parts = [dot, nm]
    if role:
        parts.append(T(role, 24, GREY).next_to(nm, DOWN, buff=0.08))
    return VGroup(*parts)


class Blob:
    """A schematic wobbling protein blob (NOT a structure): radius r(theta) = base * (1 + small waves).
    ph = animation phase, k = 0 relaxed .. 1 tense (smaller, stiffer, orange)."""

    def __init__(self, center, r=1.15, color=TEAL, k=0.0, fill=0.2):
        self.c = np.array([center[0], center[1], 0.0])
        self.r0 = r
        self.color0 = color
        self.fill = fill
        self.ph = ValueTracker(0.0)
        self.k = ValueTracker(k)
        self.ph.add_updater(lambda m, dt: m.increment_value(dt * 1.3))

    def radius(self, th):
        k = self.k.get_value()
        ph = self.ph.get_value()
        a1, a2 = (0.07 - 0.045 * k), (0.045 - 0.03 * k)
        base = self.r0 * (1 - 0.3 * k)
        return base * (1 + a1 * math.sin(3 * th + ph) + a2 * math.sin(5 * th - 1.3 * ph))

    def pt(self, th_deg):
        th = math.radians(th_deg)
        return self.c + self.radius(th) * np.array([math.cos(th), math.sin(th), 0.0])

    def color(self):
        return interpolate_color(ManimColor(self.color0), ManimColor(ORANGE), self.k.get_value())

    def make(self):
        pts = []
        for i in range(61):
            th = 2 * math.pi * i / 60
            pts.append(self.c + self.radius(th) * np.array([math.cos(th), math.sin(th), 0.0]))
        m = VMobject()
        m.set_points_smoothly(pts)
        col = self.color()
        m.set_stroke(col, 4)
        m.set_fill(col, self.fill)
        return m

    def mob(self):
        return always_redraw(self.make)


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


# ----------------------------------------------------------------------------- s01 the evening
class S01Evening(ProfileScene):
    def construct(self):
        self.add_inset()
        evening = lab("One evening", GOLD, 30).move_to([-0.4, 3.0, 0])
        self.play(pop(evening), run_time=0.45)

        room = RoundedRectangle(corner_radius=0.2, width=7.5, height=3.5, stroke_color=PLACE, stroke_width=2.5,
                                fill_color=PLACE, fill_opacity=0.07).move_to([2.55, 0.75, 0])
        room_lab = T("the lab", 28, PLACE).move_to(room.get_corner(UR) + np.array([-0.85, -0.38, 0]))
        monod = person("Monod", GOLD, [-2.0, 0.55, 0], r=0.4)
        self.at("Monod")
        self.play(pop(monod), run_time=0.4)
        self.at("walked into")
        self.play(Create(room), FadeIn(room_lab), monod.animate.move_to([0.4, 0.55, 0]), run_time=1.1)

        coat = lab("coat still on", GREY, 26).move_to([0.55, 1.6, 0])
        self.at("coat still on")
        self.play(pop(coat), run_time=0.45)

        bench = Rectangle(width=1.8, height=0.3, stroke_color=GREY, stroke_width=3, fill_color=GREY,
                          fill_opacity=0.35).move_to([2.7, 0.35, 0])
        bench_lab = T("bench", 26, GREY).next_to(bench, DOWN, buff=0.2)
        gaze = DashedLine([0.95, 0.6, 0], [1.7, 0.45, 0], color=GREY, stroke_width=3, dash_length=0.12)
        self.at("stared at the bench")
        self.play(FadeIn(bench), FadeIn(bench_lab), Create(gaze), run_time=0.7)

        ull = person("Agnès Ullmann", TEXT, [4.85, 0.55, 0], r=0.4, size=24, role="colleague")
        self.at("colleague")
        self.play(pop(ull), run_time=0.5)

        q1 = T("“I have discovered the second", 32, TEXT, font=TITLE_FONT)
        q2 = T("secret of life.”", 32, TEXT, font=TITLE_FONT)
        qg = VGroup(q1, q2).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        bubble = RoundedRectangle(corner_radius=0.25, width=qg.width + 0.7, height=qg.height + 0.55,
                                  stroke_color=GOLD, stroke_width=3, fill_color=GOLD, fill_opacity=0.1)
        bub = VGroup(bubble, qg.move_to(bubble)).move_to([2.55, -2.35, 0])
        tail = CurvedArrow(monod[0].get_bottom() + DOWN * 1.0, bubble.get_left() + LEFT * 0.05, angle=0.9,
                           color=GOLD, stroke_width=4, tip_length=0.2)
        self.at("I have discovered", lead=0.35)
        self.play(Create(tail), FadeIn(bubble), run_time=0.5)
        self.play(Write(qg), run_time=2.0)
        self.finish()


# ----------------------------------------------------------------------------- s02 two kinds of site
class S02TwoSites(ProfileScene):
    def construct(self):
        self.add_inset()

        # --- a biologist who preferred thinking to tinkering
        bio = lab("a biologist", GOLD, 30).move_to([-0.2, 2.6, 0])
        self.play(pop(bio), run_time=0.45)
        thinking = lab("thinking", GOLD, 30).move_to([-0.4, 1.3, 0])
        more = M(">", 36, GREY).move_to([1.5, 1.3, 0])
        tinker = lab("tinkering", GREY, 30).move_to([3.2, 1.3, 0])
        self.at("thinking to tinkering")
        self.play(pop(thinking), run_time=0.4)
        self.play(FadeIn(more), pop(tinker), run_time=0.4)
        strike = Line(tinker.get_left() + RIGHT * 0.05, tinker.get_right() - RIGHT * 0.05, color=GREY, stroke_width=5)
        self.play(Create(strike), tinker.animate.set_opacity(0.55), run_time=0.4)
        theories = lab("shaping theories", GOLD, 30).move_to([-0.1, 0.0, 0])
        pipe = lab("with a pipe", TEXT, 30).move_to([3.5, 0.0, 0])
        self.at("shaping theories")
        self.play(pop(theories), run_time=0.45)
        self.at("pipe")
        self.play(pop(pipe), run_time=0.45)
        others = lab(["others ran", "the bench"], GREY, 28).move_to([1.7, -1.5, 0])
        self.at("others ran the bench")
        self.play(pop(others), run_time=0.5)

        # --- clear: proteins are not rigid machines but flexible structures
        old = Group(bio, thinking, more, tinker, strike, theories, pipe, others)
        prot = lab("proteins", TEAL, 30).move_to([1.5, 2.55, 0])
        self.at("he had intuited", lead=0.15)
        self.play(FadeOut(old), run_time=0.45)
        self.play(pop(prot), run_time=0.4)
        rigid = VGroup(Rectangle(width=3.1, height=1.9, stroke_color=GREY, stroke_width=4, fill_color=GREY,
                                 fill_opacity=0.18), T("rigid machine", 26, GREY)).move_to([1.5, 0.3, 0])
        self.at("not rigid machines")
        self.play(FadeIn(rigid, scale=0.9), run_time=0.5)
        cross = xmark([1.5, 0.3, 0], size=0.9, width=9)
        self.play(Create(cross), run_time=0.4)

        blob = Blob([1.5, 0.3], 1.15, TEAL)
        self.add(blob.ph)
        bmob = blob.mob()
        flex = T("flexible structure", 28, TEAL).move_to([1.5, -1.3, 0])
        self.at("flexible structures")
        self.play(FadeOut(rigid), FadeOut(cross), run_time=0.35)
        self.add(bmob)
        self.play(FadeIn(flex, shift=UP * 0.1), run_time=0.5)

        # --- two kinds of site
        work_dot = always_redraw(lambda: Dot(blob.pt(32), radius=0.2, color=YELLOW).set_z_index(3))
        ctrl_sq = always_redraw(lambda: Square(0.36, stroke_width=0, fill_color=PURPLE, fill_opacity=1)
                                .move_to(blob.pt(-32)).set_z_index(3))
        self.at("two kinds of")
        self.play(FadeOut(flex), run_time=0.3)
        self.add(work_dot, ctrl_sq)
        self.play(FadeIn(work_dot, scale=2.0), FadeIn(ctrl_sq, scale=2.0), run_time=0.5)

        work_c = lab(["site that", "does the work"], YELLOW, 26).move_to([4.95, 1.4, 0])
        ctrl_c = lab(["site that controls", "whether the work", "can happen at all"], PURPLE, 26).move_to([4.95, -1.1, 0])
        wl = always_redraw(lambda: Line(work_dot.get_center() + RIGHT * 0.22, work_c.get_left() + LEFT * 0.05,
                                        color=YELLOW, stroke_width=3))
        cl = always_redraw(lambda: Line(ctrl_sq.get_center() + RIGHT * 0.22, ctrl_c.get_left() + LEFT * 0.05,
                                        color=PURPLE, stroke_width=3))
        self.at("one that does the work")
        self.add(wl)
        self.play(pop(work_c), run_time=0.5)
        self.play(Indicate(work_dot, color=YELLOW, scale_factor=1.5), run_time=0.6)
        self.at("one that controls")
        self.add(cl)
        self.play(pop(ctrl_c), run_time=0.5)
        self.play(Indicate(ctrl_sq, color=PURPLE, scale_factor=1.5), run_time=0.6)

        # --- he named the effect allostery but had no mechanism
        allo = lab("allostery", GOLD, 30).move_to([-1.3, 0.3, 0])
        link = Arrow(allo.get_right() + RIGHT * 0.05, [0.25, 0.3, 0], color=GOLD, stroke_width=4, buff=0,
                     max_tip_length_to_length_ratio=0.35)
        self.at("named the effect")
        self.play(pop(allo), GrowArrow(link), run_time=0.6)
        nomech = dashed(lab("no mechanism", GREY, 30), GREY).move_to([1.5, -2.55, 0])
        self.at("no mechanism")
        self.play(FadeIn(nomech, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s03 the blackboard
class S03Blackboard(ProfileScene):
    def construct(self):
        self.add_inset()
        picture = lab("the picture", GOLD, 30).move_to([0.4, 2.6, 0])
        proof = lab("its proof", WYMAN, 30).move_to([3.9, 2.6, 0])
        self.at("picture")
        self.play(pop(picture), run_time=0.4)
        self.at("proof")
        self.play(pop(proof), run_time=0.4)

        monod = person("Monod", GOLD, [0.4, 1.1, 0])
        wyman = person("Jeffries Wyman", WYMAN, [3.9, 1.1, 0], size=26, role="thermodynamicist")
        self.at("he and")
        self.play(pop(monod), run_time=0.4)
        self.at("thermodynamicist")
        self.play(pop(wyman), run_time=0.5)

        board = RoundedRectangle(corner_radius=0.12, width=5.6, height=1.35, stroke_color=PLACE, stroke_width=3,
                                 fill_color=PLACE, fill_opacity=0.1).move_to([2.15, -1.7, 0])
        board_lab = T("blackboard", 30, PLACE).move_to(board)
        a1 = Arrow([0.4, -0.1, 0], [0.9, -0.95, 0], color=GOLD, stroke_width=4, buff=0, max_tip_length_to_length_ratio=0.3)
        a2 = Arrow([3.9, -0.42, 0], [3.4, -0.95, 0], color=WYMAN, stroke_width=4, buff=0, max_tip_length_to_length_ratio=0.3)
        self.at("met over")
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.5)
        self.play(Create(board), FadeIn(board_lab), run_time=0.6)

        pasteur = lab("Institut Pasteur", PLACE, 28).move_to([2.15, -3.0, 0])
        self.at("Pasteur", lead=0.5)
        self.play(pop(pasteur), run_time=0.5)
        yr = M("1964", 40, GOLD, weight=BOLD).move_to([5.3, -3.0, 0])
        self.at("1964")
        self.play(Write(yr), run_time=0.5)

        # --- the biologist had the picture and no proof; the thermodynamicist the proof and no picture
        stage = Group(picture, proof, monod, wyman, board, board_lab, a1, a2, pasteur, yr)
        self.at("The biologist", lead=0.45)
        self.play(FadeOut(stage), run_time=0.4)
        bio = person("the biologist", GOLD, [0.2, 2.1, 0], size=28)
        self.play(FadeIn(bio, shift=UP * 0.1), run_time=0.4)
        pic = lab("the picture", GOLD, 30).move_to([0.2, 0.5, 0])
        self.at("had the picture")
        self.play(pop(pic), run_time=0.45)
        nop = dashed(lab("no proof", WYMAN, 30), WYMAN).move_to([0.2, -0.9, 0])
        self.at("no proof")
        self.play(FadeIn(nop, shift=UP * 0.1), run_time=0.45)

        thermo = person("the thermodynamicist", WYMAN, [4.5, 2.1, 0], size=26)
        self.at("The thermodynamicist", nth=1)
        self.play(FadeIn(thermo, shift=UP * 0.1), run_time=0.45)
        pr = lab("the proof", WYMAN, 30).move_to([4.5, 0.5, 0])
        self.at("had the proof")
        self.play(pop(pr), run_time=0.45)
        nopic = dashed(lab("no picture", GOLD, 30), GOLD).move_to([4.5, -0.9, 0])
        self.at("no picture")
        self.play(FadeIn(nopic, shift=UP * 0.1), run_time=0.45)
        self.finish()


# ----------------------------------------------------------------------------- s04 the MWC model
class S04Mwc(ProfileScene):
    def construct(self):
        self.add_inset()
        ay = 3.0
        axis = Arrow([-2.2, ay, 0], [6.15, ay, 0], color=GREY, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.04)
        d1, d2 = Dot([-0.6, ay, 0], radius=0.12, color=GOLD), Dot([4.6, ay, 0], radius=0.12, color=GOLD)
        y64 = M("1964", 30, GOLD, weight=BOLD).next_to(d1, DOWN, buff=0.2)
        y65 = M("1965", 30, GOLD, weight=BOLD).next_to(d2, DOWN, buff=0.2)
        self.play(Create(axis), FadeIn(d1, scale=2), FadeIn(y64), run_time=0.6)

        mwc = lab("the MWC model", GOLD, 32).move_to([1.95, 1.6, 0])
        self.at("austere")
        self.play(pop(mwc), run_time=0.5)

        tense = Blob([4.1, -0.1], 1.0, TEAL, k=1.0)
        relaxed = Blob([-0.2, -0.1], 1.0, TEAL, k=0.0)
        self.add(tense.ph, relaxed.ph)
        tm, rm = tense.mob(), relaxed.mob()
        tl = T("tense", 30, ORANGE).move_to([4.1, -1.25, 0])
        rl = T("relaxed", 30, TEAL).move_to([-0.2, -1.42, 0])
        swap = DoubleArrow([1.0, -0.1, 0], [2.9, -0.1, 0], color=GREY, stroke_width=4, buff=0, tip_length=0.2)
        two = T("two states", 28, GREY).move_to([1.95, 0.45, 0])
        self.at("two state")
        self.add(tm, rm)
        self.play(FadeIn(tl), FadeIn(rl), GrowFromCenter(swap), FadeIn(two), run_time=0.8)

        ry = -2.3
        mon = person("Monod", GOLD, [-1.4, ry, 0], r=0.26, size=26)
        wy = person("Wyman", WYMAN, [1.0, ry, 0], r=0.26, size=26)
        chx = person("Jean-Pierre Changeux", GREEN, [4.3, ry, 0], r=0.26, size=24, role="the young")
        l1 = Line(mon[0].get_right() + RIGHT * 0.12, wy[0].get_left() + LEFT * 0.12, color=GREY, stroke_width=3)
        l2 = Line(wy[0].get_right() + RIGHT * 0.12, chx[0].get_left() + LEFT * 0.12, color=GREY, stroke_width=3)
        self.at("written with")
        self.play(pop(mon), pop(wy), Create(l1), run_time=0.5)
        self.at("the young")
        self.play(Create(l2), pop(chx), run_time=0.5)
        self.at("1965")
        self.play(FadeIn(d2, scale=2), FadeIn(y65), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s05 the Bohr effect
class S05Bohr(ProfileScene):
    def construct(self):
        self.add_inset()
        bohr = lab("the Bohr effect", GOLD, 32).move_to([1.2, 3.0, 0])
        self.at("Bohr")
        self.play(pop(bohr), run_time=0.5)

        blob = Blob([0.9, 0.7], 1.15, TEAL, k=0.15)
        self.add(blob.ph)
        bm = blob.mob()
        hb = T("hemoglobin", 28, TEAL).move_to([0.9, 2.15, 0])
        muscle = lab(["working", "muscle"], PINK, 28).move_to([5.0, 0.7, 0])
        ox = VGroup(*[Dot(blob.c + np.array([dx, dy, 0]), radius=0.13, color=TEXT)
                      for dx, dy in ((-0.25, 0.2), (0.2, 0.3), (0.0, -0.1))]).set_z_index(2)
        self.add(bm)
        self.play(FadeIn(ox, scale=0.5), run_time=0.4)

        acid_lab = T("acid", 28, RED, weight=BOLD).move_to([3.1, 1.45, 0])
        self.at("where acid")
        self.play(pop(muscle), run_time=0.4)
        drops = VGroup(*[Dot([3.7 - 0.0, 0.7 + dy, 0], radius=0.14, color=RED) for dy in (-0.4, 0.0, 0.4)])
        self.at("acid from", lead=0.0)
        self.play(FadeIn(acid_lab), FadeIn(drops), run_time=0.3)
        self.play(LaggedStart(*[d.animate.shift(LEFT * 1.05) for d in drops], lag_ratio=0.15), run_time=0.8)

        # the balance: relaxed <-> tense slider
        ty = -1.45
        x_l, x_r = -0.6, 2.8
        track = Line([x_l, ty, 0], [x_r, ty, 0], color=GREY, stroke_width=4)
        rl = T("relaxed", 28, TEAL).move_to([x_l - 0.95, ty, 0])
        tl = T("tense", 28, ORANGE).move_to([x_r + 0.8, ty, 0])
        mark = always_redraw(lambda: Dot([x_l + (x_r - x_l) * blob.k.get_value(), ty, 0], radius=0.2,
                                         color=interpolate_color(ManimColor(TEAL), ManimColor(ORANGE),
                                                                 blob.k.get_value())).set_z_index(3))
        self.at("tips hemoglobin")
        self.play(FadeIn(hb, shift=UP * 0.1), Create(track), FadeIn(rl), FadeIn(tl), FadeOut(drops), FadeOut(acid_lab),
                  run_time=0.6)
        self.add(mark)
        self.at("toward the tense")
        self.play(blob.k.animate.set_value(0.95), run_time=1.3, rate_func=smooth)
        self.play(Indicate(tl, color=ORANGE, scale_factor=1.2), run_time=0.3)

        # oxygen falls out
        ox_lab = T("oxygen", 28, TEXT).move_to([2.9, 0.05, 0])
        self.at("oxygen")
        self.play(FadeIn(ox_lab, shift=UP * 0.1), LaggedStart(*[d.animate.shift(RIGHT * 2.1)
                                                                 for d in ox], lag_ratio=0.2), run_time=0.8)

        self.at("exactly where")
        strain = lab(["straining", "muscle"], PINK, 28).move_to(muscle)
        self.play(Transform(muscle, strain), run_time=0.5)
        self.play(Indicate(muscle, color=PINK, scale_factor=1.12), run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------- s06 the quote
class S06Quote(ProfileScene):
    def construct(self):
        self.add_inset()
        lines = ["“I have discovered the", "second secret of life.”"]
        q = VGroup(*[T(l, 44, TEXT, font=TITLE_FONT) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        fit(q, max_w=8.4)
        who = T("— Jacques Monod", 32, GOLD)
        to = T("to his colleague Agnès Ullmann", 26, GREY)
        g = VGroup(q, VGroup(who, to).arrange(DOWN, aligned_edge=RIGHT, buff=0.15)).arrange(DOWN, aligned_edge=RIGHT, buff=0.55)
        g.move_to([PANEL_C, 0.1, 0])
        for ln in q:
            ln.set_opacity(0)
        att = g[1]
        att.set_opacity(0)
        self.add(g)
        self.wait(0.4)
        for ln in q:
            self.play(ln.animate.set_opacity(1.0), run_time=0.9)
        self.wait(0.4)
        self.play(att.animate.set_opacity(1.0), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s07 end card
class S07End(EndCard):
    LINE = "Coined allostery; co-built the MWC two-state model, explaining hemoglobin cooperativity."

    def construct(self):
        a = T("Coined allostery; co-built the MWC two-state model,", size=40, font=TITLE_FONT)
        b = T("explaining hemoglobin cooperativity.", size=40, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.22)
        fit(line, max_w=11.8)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
