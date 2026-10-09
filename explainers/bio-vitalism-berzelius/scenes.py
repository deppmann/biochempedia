"""Jöns Jacob Berzelius: a scientist profile (Biochemistrypedia, vitalism lesson).

Narration is the lesson entry's `story`, verbatim (three sentences = three tts scenes). Everything on
screen comes from that entry (name, dates, contribution, story, quote). The portrait is an
AI-generated engraving-style illustration from The Molecule Hunters, captioned
"illustration · AI-generated" whenever it is on screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = Berzelius: portrait frame, name/dates, his lab, his verdict, the firmest line, his value
  PLACE  = places: Europe, Stockholm (lavender, not BLUE: too close to TEAL)
  BLUE   = atomic weights: the forty-five measured elements, the "few percent" band
  YELLOW = the reference / the assignment: today's value, Wöhler's first assigned analysis
  RED    = speed and the harsh verdict's target (raced, speed)
  TEAL   = care (the missing half of "speed without care")
  GREEN  = organic kingdom        AMBER = inorganic kingdom
  TEXT   = Wöhler (white)         GREY  = structure, labels, the unmeasured five
No molecular structure is drawn: the lab is a schematic floor plan, the elements are plain tiles.
"""
import os
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

config.disable_caching = True

PORTRAIT = str(Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent / "berz_up.png")
CAPTION = "illustration · AI-generated"
PLACE = "#B39DDB"
AMBER = "#E0A458"
NAME = "Jöns Jacob Berzelius"
DATES = "1779–1848"

INSET_C = np.array([-4.6, 1.15, 0.0])
INSET_H = 3.2
CX = 1.95            # x centre of the right panel (x from -2.4 to 6.3)


# ----------------------------------------------------------------------------- helpers
def portrait_pair(height):
    img = ImageMobject(PORTRAIT).set_height(height)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["cubic"])
    frame = Rectangle(width=img.width, height=img.height, stroke_color=GOLD, stroke_width=3, fill_opacity=0)
    return img, frame


def caption_under(frame, size=22):
    return T(CAPTION, size=size, color=GREY, font=TITLE_FONT).next_to(frame, DOWN, buff=0.2)


def name_tag(frame):
    nm = T("Jöns Jacob", size=32, font=TITLE_FONT)
    nm2 = T("Berzelius", size=32, font=TITLE_FONT)
    dt = T(DATES, size=28, color=GOLD)
    g = VGroup(nm, nm2, dt).arrange(DOWN, buff=0.1)
    g.move_to([frame.get_center()[0], frame.get_center()[1] - INSET_H / 2 - 1.35, 0])
    return g


def inset_group():
    img, frame = portrait_pair(INSET_H)
    img.move_to(INSET_C)
    frame.move_to(INSET_C)
    cap = caption_under(frame)
    tag = name_tag(frame)
    rule = Line([-2.7, -3.2, 0], [-2.7, 3.2, 0], color=GREY, stroke_width=1.5).set_opacity(0.35)
    return img, frame, cap, tag, rule


def box(lines, color=BLUE, size=28, pad=0.22, fill=0.16, dashed=False):
    """Chip with one or more centered lines of text."""
    if isinstance(lines, str):
        lines = [lines]
    txt = VGroup(*[T(l, size, color) for l in lines]).arrange(DOWN, buff=0.1)
    ref_h = len(lines) * T("Ag", size).height + (len(lines) - 1) * 0.1
    rr = RoundedRectangle(corner_radius=0.14, width=txt.width + 2 * pad, height=max(txt.height, ref_h) + 2 * pad,
                          stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=fill)
    if dashed:
        rr = DashedVMobject(RoundedRectangle(corner_radius=0.14, width=txt.width + 2 * pad,
                                             height=max(txt.height, ref_h) + 2 * pad, stroke_color=color,
                                             stroke_width=2.5), num_dashes=40, dashed_ratio=0.55).set_color(color)
        return VGroup(rr, txt.move_to(rr.get_center()))
    return VGroup(rr, txt.move_to(rr))


def pop(mob):
    return FadeIn(mob, shift=UP * 0.12)


class ProfileScene(SpokenScene):
    def add_inset(self):
        img, frame, cap, tag, rule = inset_group()
        self.add(img, frame, cap, tag, rule)

    def hold(self, extra=1.5):
        """Keep the finished picture up for a beat after the last word."""
        rest = self.narration_s + extra - self.elapsed()
        if rest > 0:
            self.wait(rest)
        self.finish()


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
        name = T(self.TITLE, size=50, font=TITLE_FONT)
        dates = T(DATES, size=38, color=GOLD)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        txt = VGroup(brand, lesson, name, dates, rule).arrange(DOWN, buff=0.3).move_to([3.2, 0.2, 0])
        self.play(FadeIn(img), FadeIn(frame), FadeIn(cap), run_time=0.5)
        self.play(
            ScaleInPlace(grp, 1.08, run_time=4.4, rate_func=linear),
            Succession(
                Wait(0.3),
                FadeIn(VGroup(brand, lesson), shift=UP * 0.1, run_time=0.5),
                Write(name, run_time=1.0),
                FadeIn(dates, shift=UP * 0.1, run_time=0.5),
                GrowFromCenter(rule, run_time=0.4),
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


# ----------------------------------------------------------------------------- s01 the laboratory
class S01Lab(ProfileScene):
    def construct(self):
        self.add_inset()
        # --- the most respected laboratory in Europe
        lab = box("Berzelius’s laboratory", GOLD, 32).move_to([CX, 2.75, 0])
        self.play(pop(lab), run_time=0.5)
        txt = T("the most respected in", 28, TEXT)
        eu = box("Europe", PLACE, 28)
        row = VGroup(txt, eu).arrange(RIGHT, buff=0.3).move_to([CX, 1.8, 0])
        self.at("most respected")
        self.play(FadeIn(txt, shift=UP * 0.1), run_time=0.4)
        self.at("Europe")
        self.play(pop(eu), run_time=0.4)

        # --- a converted apartment kitchen (schematic floor plan)
        rx, ry = 0.55, -0.55
        room = Rectangle(width=4.7, height=2.5, stroke_color=GREY, stroke_width=3).move_to([rx, ry, 0])
        counter = Rectangle(width=4.7, height=0.24, stroke_width=0, fill_color=GREY, fill_opacity=0.4)
        counter.move_to([rx, ry - 1.25 + 0.12, 0])
        rlab = VGroup(T("converted apartment", 30, TEXT), T("kitchen", 30, TEXT)).arrange(DOWN, buff=0.08)
        rlab.move_to([rx, ry + 0.15, 0])
        self.at("converted apartment kitchen")
        self.play(Create(room), FadeIn(counter), run_time=0.6)
        self.play(FadeIn(rlab, shift=UP * 0.1), run_time=0.4)
        self.at("Stockholm")
        sto = box("Stockholm", PLACE, 32).move_to([4.85, ry, 0])
        link = Line(room.get_right(), sto.get_left(), color=PLACE, stroke_width=3)
        self.play(Create(link), pop(sto), run_time=0.5)

        # --- clear; the atomic weights of 45 of 50 elements
        self.at("determining", lead=0.4)
        self.play(FadeOut(Group(lab, row, room, counter, rlab, link, sto)), run_time=0.35)
        tiles = VGroup(*[RoundedRectangle(corner_radius=0.06, width=0.5, height=0.5, stroke_color=GREY, stroke_width=2,
                                          fill_color=GREY, fill_opacity=0.08) for _ in range(50)])
        tiles.arrange_in_grid(rows=5, cols=10, buff=0.12).move_to([CX, 0.55, 0])
        hA = T("atomic weights of", 26, BLUE)
        hB = M("45", 36, BLUE)
        hC1 = T("of the 50", 26, GREY)
        hC2 = T("known elements", 26, GREY)
        head = VGroup(hA, hB, hC1, hC2).arrange(RIGHT, buff=0.22, aligned_edge=DOWN).move_to([CX, 2.75, 0])
        assert head.width <= 8.6, head.width
        self.at("atomic weights")
        self.play(FadeIn(hA, shift=UP * 0.1), LaggedStart(*[FadeIn(t, scale=0.8) for t in tiles], lag_ratio=0.02),
                  run_time=1.0)
        self.at("45", lead=0.3)
        self.play(FadeIn(hB, shift=UP * 0.1),
                  LaggedStart(*[t.animate.set_stroke(BLUE).set_fill(BLUE, 0.55) for t in tiles[:45]], lag_ratio=0.015),
                  run_time=0.8)
        self.at("of the 50", lead=0.1)
        self.play(FadeIn(hC1, shift=UP * 0.1),
                  *[Indicate(t, color=TEXT, scale_factor=1.25) for t in tiles[45:]], run_time=0.6)
        self.at("known elements", lead=0.1)
        self.play(FadeIn(hC2, shift=UP * 0.1), run_time=0.4)

        # --- within a few percent of today's values
        ly = -2.3
        axis = Line([CX - 2.7, ly, 0], [CX + 2.7, ly, 0], color=GREY, stroke_width=3)
        band = Rectangle(width=1.5, height=0.55, stroke_width=0, fill_color=BLUE, fill_opacity=0.35).move_to([CX, ly, 0])
        blab = T("within a few percent", 26, BLUE).move_to([CX, ly + 0.62, 0])
        self.at("within a few percent", lead=0.25)
        self.play(Create(axis), FadeIn(band), FadeIn(blab, shift=UP * 0.1), run_time=0.7)
        tick = Line([CX, ly - 0.45, 0], [CX, ly + 0.45, 0], color=YELLOW, stroke_width=5)
        tl = T("today’s value", 26, YELLOW).move_to([CX + 1.4, ly - 0.62, 0])
        dot = Dot([CX - 0.28, ly, 0], radius=0.13, color=GOLD)
        dl = T("his value", 26, GOLD).move_to([CX - 1.15, ly - 0.62, 0])
        self.at("today's values", lead=0.25)
        self.play(Create(tick), FadeIn(tl, shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(dot, scale=2.0), FadeIn(dl, shift=UP * 0.1), run_time=0.5)
        self.hold(1.4)


# ----------------------------------------------------------------------------- s02 the verdict
class S02Verdict(ProfileScene):
    def construct(self):
        self.add_inset()
        woh = box("young Wöhler", TEXT, 30).move_to([-0.5, 2.8, 0])
        self.play(pop(woh), run_time=0.5)

        # --- he raced through his first assigned analysis
        ty = 1.55
        track = Line([-1.6, ty, 0], [5.4, ty, 0], color=GREY, stroke_width=3)
        finish = Square(0.3, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9).move_to([5.4, ty, 0])
        runner = Dot([-1.6, ty, 0], radius=0.17, color=TEXT)
        trail = Line([-1.6, ty, 0], [-1.6, ty, 0], color=RED, stroke_width=6)
        raced = T("raced", 28, RED).move_to([1.9, ty - 0.55, 0])
        self.at("raced")
        self.play(Create(track), FadeIn(finish), FadeIn(runner), run_time=0.3)
        trail.add_updater(lambda m: m.put_start_and_end_on([-1.6, ty, 0], runner.get_center()))
        self.add(trail)
        ana = box("first assigned analysis", YELLOW, 28).move_to([3.95, 2.8, 0])
        self.play(runner.animate.move_to([5.4, ty, 0]), FadeIn(raced),
                  Succession(Wait(0.6), pop(ana)), run_time=1.3, rate_func=rush_into)
        trail.clear_updaters()

        # --- Berzelius hands down the verdict, which trails him for life
        self.at("handed down")
        ber = box("Berzelius", GOLD, 30).move_to([-0.5, 0.0, 0])
        self.play(pop(ber), run_time=0.5)
        self.at("verdict")
        arr = Arrow(ber.get_right() + RIGHT * 0.1, [2.2, 0.0, 0], buff=0, color=GOLD, stroke_width=5,
                    max_tip_length_to_length_ratio=0.3)
        ver = box("verdict", GOLD, 32, fill=0.3).move_to([3.5, 0.0, 0])
        self.play(GrowArrow(arr), FadeIn(ver, scale=0.9), run_time=0.6)

        self.at("trailed him")
        ly = -1.7
        life = Arrow([-1.9, ly, 0], [6.0, ly, 0], color=GREY, stroke_width=3, buff=0, max_tip_length_to_length_ratio=0.04)
        wdot = Dot([-0.2, ly, 0], radius=0.17, color=TEXT)
        tag = box("verdict", GOLD, 24, pad=0.14, fill=0.3)
        tag.move_to([-0.2 - 1.45, ly + 0.5, 0])
        tether = DashedLine(tag.get_right(), wdot.get_left(), color=GOLD, stroke_width=3)
        mover = VGroup(tag, tether, wdot)
        self.play(Create(life), ReplacementTransform(ver, tag), FadeOut(arr), FadeIn(tether), FadeIn(wdot), run_time=0.45)
        fl = T("for life", 28, GOLD).move_to([4.6, ly - 0.65, 0])
        self.play(mover.animate.shift(RIGHT * 5.0), Succession(Wait(0.25), FadeIn(fl, shift=UP * 0.1)),
                  run_time=1.0, rate_func=smooth)

        # --- speed without care counts for nothing
        self.at("Speed", lead=0.55)
        self.play(FadeOut(Group(woh, track, finish, runner, trail, raced, ana, ber, life, mover, fl)), run_time=0.3)
        spd = box("speed", RED, 40)
        wo = T("without", 32, RED)
        care = box("care", TEAL, 40, dashed=True)
        row = VGroup(spd, wo, care).arrange(RIGHT, buff=0.45).move_to([CX, 0.9, 0])
        self.at("Speed", lead=0.0)
        self.play(pop(spd), run_time=0.4)
        self.at("without care", lead=0.1)
        self.play(FadeIn(wo, shift=UP * 0.1), run_time=0.3)
        self.at("care", lead=0.05)
        self.play(FadeIn(care, scale=0.9), run_time=0.4)
        self.at("counts for nothing", lead=0.1)
        arrow = Arrow([CX, 0.2, 0], [CX, -0.75, 0], buff=0, color=GOLD, stroke_width=5, max_tip_length_to_length_ratio=0.35)
        nothing = T("counts for nothing", 48, GOLD, font=TITLE_FONT).move_to([CX, -1.55, 0])
        self.play(GrowArrow(arrow), Write(nothing), run_time=1.1)
        ul = Line(nothing.get_corner(DL) + DOWN * 0.1, nothing.get_corner(DR) + DOWN * 0.1, color=GOLD, stroke_width=4)
        self.play(Create(ul), run_time=0.4)
        self.hold(1.4)


# ----------------------------------------------------------------------------- s03 the firmest line
class S03Line(ProfileScene):
    def construct(self):
        self.add_inset()
        wy0, wy1 = -1.6, 1.3     # wall from y0 to y1
        left_c, right_c = -0.1, 4.0
        wall = Line([CX, wy0, 0], [CX, wy1, 0], color=GOLD, stroke_width=9)
        self.play(Create(wall), run_time=0.7)
        self.at("firmest")
        fl = T("the firmest line of the age", 32, GOLD, font=TITLE_FONT).move_to([CX, wy0 - 0.55, 0])
        self.play(FadeIn(fl, shift=UP * 0.1), run_time=0.6)

        # --- organic versus inorganic
        band_l = Rectangle(width=4.05, height=wy1 - wy0, stroke_width=0, fill_color=GREEN, fill_opacity=0.09)
        band_l.move_to([CX - 0.1 - 2.025, (wy0 + wy1) / 2, 0])
        band_r = Rectangle(width=4.05, height=wy1 - wy0, stroke_width=0, fill_color=AMBER, fill_opacity=0.09)
        band_r.move_to([CX + 0.1 + 2.025, (wy0 + wy1) / 2, 0])
        org = box("organic", GREEN, 36).move_to([left_c, 0.35, 0])
        ino = box("inorganic", AMBER, 36).move_to([right_c, 0.35, 0])
        self.at("organic", lead=0.15)
        self.play(FadeIn(band_l), pop(org), run_time=0.5)
        self.at("inorganic", lead=0.15)
        self.play(FadeIn(band_r), pop(ino), run_time=0.5)

        # --- two kingdoms under separate laws
        self.at("two kingdoms", lead=0.15)
        kl = T("kingdom", 28, GREEN).move_to([left_c, -0.45, 0])
        kr = T("kingdom", 28, AMBER).move_to([right_c, -0.45, 0])
        self.play(FadeIn(kl, shift=UP * 0.1), FadeIn(kr, shift=UP * 0.1), run_time=0.5)
        self.at("separate laws", lead=0.25)
        ll = box("its own laws", GREEN, 26, dashed=True).move_to([left_c, -1.15, 0])
        lr = box("its own laws", AMBER, 26, dashed=True).move_to([right_c, -1.15, 0])
        neq_bg = Circle(radius=0.3, stroke_color=GOLD, stroke_width=3, fill_color=BG, fill_opacity=1).move_to([CX, -0.4, 0])
        neq = M("≠", 34, GOLD).move_to(neq_bg)
        self.play(FadeIn(ll, shift=UP * 0.1), FadeIn(lr, shift=UP * 0.1), FadeIn(neq_bg), FadeIn(neq), run_time=0.7)

        # --- his whole system rested on it
        self.at("his whole system", lead=0.25)
        slab_box = RoundedRectangle(corner_radius=0.14, width=7.0, height=0.8, stroke_color=GOLD, stroke_width=3,
                                    fill_color=GOLD, fill_opacity=0.25)
        slab = VGroup(slab_box, T("his whole system", 32, GOLD, font=TITLE_FONT).move_to(slab_box))
        slab.move_to([CX, wy1 + 0.45 + 0.9, 0])
        self.play(FadeIn(slab, shift=DOWN * 0.9), run_time=0.7)
        self.at("rested on it", lead=0.1)
        # the slab settles onto the top of the wall: the system rests on the line
        self.play(slab.animate.shift(DOWN * (slab.get_bottom()[1] - wy1)), run_time=0.6, rate_func=rush_into)
        self.play(Indicate(wall, color=TEXT, scale_factor=1.06), run_time=0.6)
        self.hold(1.5)


# ----------------------------------------------------------------------------- s04 what he gave (silent)
class S04Gave(ProfileScene):
    def construct(self):
        self.add_inset()
        head = T("Gave chemistry its written alphabet", 36, TEXT, font=TITLE_FONT).move_to([CX, 2.95, 0])
        fit(head, max_w=8.5)
        self.wait(0.2)
        self.play(Write(head), run_time=1.3)
        wy0, wy1 = -1.5, 1.4
        wall = Line([CX, wy0, 0], [CX, wy1, 0], color=GOLD, stroke_width=9)
        lbl = T("the era’s sharpest line", 28, GOLD).move_to([CX, wy1 + 0.45, 0])
        org = box("organic matter", GREEN, 28).move_to([CX - 2.15, 0.9, 0])
        ino = box("inorganic matter", AMBER, 28).move_to([CX + 2.15, 0.9, 0])
        self.wait(0.2)
        self.play(Create(wall), FadeIn(lbl, shift=UP * 0.1), run_time=0.8)
        self.play(pop(org), pop(ino), run_time=0.5)
        # his student walks across the wall
        # Wöhler went from an inorganic salt to an organic product: right (inorganic) to left (organic)
        sdot = Dot(radius=0.2, color=TEXT).move_to([CX + 3.4, -0.35, 0])
        slab = T("his student", 26, TEXT).next_to(sdot, UP, buff=0.2)
        self.play(FadeIn(sdot), FadeIn(slab), run_time=0.4)
        self.play(FadeOut(slab), run_time=0.25)
        self.play(sdot.animate.move_to([CX - 3.4, -0.35, 0]), run_time=1.4, rate_func=smooth)
        slab2 = T("his student", 26, TEXT).next_to(sdot, UP, buff=0.2)
        self.play(FadeIn(slab2), run_time=0.3)
        fin = T("the very wall his student would walk across", 28, TEXT).move_to([CX, -2.4, 0])
        self.play(FadeIn(fin, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s05 quote (silent)
class S05Quote(ProfileScene):
    def construct(self):
        self.add_inset()
        lines = ["“Doctor, that was quickly", "and badly done.”"]
        q = VGroup(*[T(l, 48, TEXT, font=TITLE_FONT) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        fit(q, max_w=8.4)
        who = T("— Jöns Jacob Berzelius", 32, GOLD)
        wg = VGroup(who)
        g = VGroup(q, wg).arrange(DOWN, aligned_edge=RIGHT, buff=0.6).move_to([CX, 0.1, 0])
        for ln in q:
            ln.set_opacity(0)
        wg.set_opacity(0)
        self.add(g)
        self.wait(0.4)
        for ln in q:
            self.play(ln.animate.set_opacity(1.0), run_time=0.9)
        self.wait(0.5)
        self.play(wg.animate.set_opacity(1.0), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- s06 end card
class S06End(EndCard):
    LINE = "Gave chemistry its written alphabet; drew the organic–inorganic line Wöhler crossed."

    def construct(self):
        img, frame = portrait_pair(2.3)
        grp = Group(img, frame).move_to([0, 2.05, 0])
        cap = T(CAPTION, 22, GREY, font=TITLE_FONT).next_to(frame, DOWN, buff=0.15)
        a = T("Gave chemistry its written alphabet;", size=40, font=TITLE_FONT)
        b = T("drew the organic–inorganic line Wöhler crossed.", size=40, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.2).move_to([0, -0.6, 0])
        fit(line, max_w=11.5)
        sub = T("biochemistrypedia.com", 24, TEAL).move_to([0, -1.9, 0])
        src = T("Source: The Molecule Hunters, Part I · “A Language for Matter”", 22, GREY).move_to([0, -2.65, 0])
        self.play(FadeIn(img), FadeIn(frame), FadeIn(cap), run_time=0.6)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=0.8)
        self.play(FadeIn(sub), FadeIn(src), run_time=0.5)
        self.finish()
