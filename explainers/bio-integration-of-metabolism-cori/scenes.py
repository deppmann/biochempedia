"""Carl & Gerty Cori: scientist profile video (Biochemistrypedia, integration-of-metabolism lesson)

This film follows THIS lesson entry's story: the Coris' question about where a sprinting muscle's
lactate goes, the muscle -> blood -> liver -> glucose -> back circuit, "the first inter-organ cycle",
and Gerty as the first woman to win the Nobel Prize in Medicine.
The portrait (public/scientists/cori.png, an AI-generated engraving-style illustration from
The Molecule Hunters) is the anchor: the title scene pushes in on it, then it stays as a framed
inset on the left while the right side animates the story's beats as the narrator reaches them.
Every cue is a self.at("spoken words") lookup in audio/words.json (word timestamps of the real audio).
Nothing on screen adds a fact that is not in the lesson entry (name, dates, contribution, story, quotes).

COLOR MAP (one color per concept, whole video)
  GOLD   = the Coris, the portrait frame, "a circuit", the cycle, first woman / Nobel
  RED    = muscle
  BLUE   = liver
  AMBER  = lactate
  GREEN  = glucose / fuel / the sugar being measured
  GREY   = blood, structure, labels, "physiology", "hand-waved"
  TEAL   = brand
"""
import os
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

config.disable_caching = True

AMBER = "#E0A458"
CX = 1.9            # centre of the content area to the right of the portrait column
PORT_X = -4.8      # portrait column centre
PORT_H = 3.5
PORT_Y = 1.25
CROP_AR = 800 / 760.0   # cori_crop.png: both faces complete (cropped from public/scientists/cori.png)
IMG = Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent / "cori_crop.png"
NAME = "Carl & Gerty Cori"
DATES = "1896–1984 · 1896–1957"
CAPTION = "illustration · AI-generated"
DIM = 0.62

# loop diagram geometry (shared by s02, s03, s04)
MX, LX = -0.7, 4.6          # muscle / liver box centres
BW, BH = 2.4, 2.4
TOP_Y, BOT_Y = 0.55, -0.55  # arrow rows


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
    dl, dr, nl, nr = plate
    return [dl.animate.set_fill(BG, opacity=DIM if which == "right" else 0),
            dr.animate.set_fill(BG, opacity=DIM if which == "left" else 0),
            nl.animate.set_opacity(0.4 if which == "right" else 1),
            nr.animate.set_opacity(0.4 if which == "left" else 1)]


def box(label, color, cx):
    r = RoundedRectangle(corner_radius=0.2, width=BW, height=BH, stroke_color=color, stroke_width=3,
                         fill_color=color, fill_opacity=0.12).move_to([cx, 0, 0])
    t = T(label, 28, color, weight=BOLD).move_to([cx, BH / 2 - 0.4, 0])
    return VGroup(r, t)


def arrow(y, left_to_right, color=GREY):
    a, b = [MX + BW / 2 + 0.05, y, 0], [LX - BW / 2 - 0.05, y, 0]
    if not left_to_right:
        a, b = b, a
    return Arrow(a, b, buff=0, color=color, stroke_width=5, max_tip_length_to_length_ratio=0.12)


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

    def static_loop(self, interior=True):
        """The finished circuit of s02, placed instantly so later scenes continue from it."""
        mus, liv = box("muscle", RED, MX), box("liver", BLUE, LX)
        top, bot = arrow(TOP_Y, True), arrow(BOT_Y, False)
        blood = T("blood", 26, GREY).move_to([(MX + LX) / 2, 0, 0])
        lac = self.chip_at("lactate", AMBER, (MX + LX) / 2, 1.35, 26)
        glu = self.chip_at("glucose", GREEN, (MX + LX) / 2, -1.35, 26)
        self.add(mus, liv, top, bot, blood, lac, glu)
        return mus, liv, top, bot, blood, lac, glu


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
        name.move_to([0, -2.45, 0])
        dates = T(DATES, 28, GOLD).move_to([0, -3.4, 0])
        rule = Line(LEFT * 1.0, RIGHT * 1.0, color=GOLD, stroke_width=4).move_to([0, -3.0, 0])

        self.play(FadeIn(img), FadeIn(border), FadeIn(brand), FadeIn(cap), run_time=0.4)
        self.play(img.animate.scale(1.05), border.animate.scale(1.05),
                  Write(name, run_time=1.0), run_time=2.0, rate_func=linear)
        self.play(GrowFromCenter(rule), FadeIn(dates), run_time=0.35)
        self.wait(0.4)
        cap2, nl, nr = column_labels()
        self.play(AnimationGroup(
            img.animate.scale(1 / (k * 1.05)).move_to([PORT_X, PORT_Y, 0]),
            border.animate.scale(1 / (k * 1.05)).move_to([PORT_X, PORT_Y, 0]),
            cap.animate.move_to(cap2),
            Succession(AnimationGroup(FadeOut(name), FadeOut(dates), FadeOut(rule), FadeOut(brand)),
                       AnimationGroup(FadeIn(nl), FadeIn(nr))),
            run_time=0.8))
        self.finish()


class S01Question(BioScene):
    def construct(self):
        self.add_column("both")
        # --- a question physiology had only hand-waved at
        self.at("question")
        q = T("?", 110, GOLD, font=TITLE_FONT).move_to([-1.5, 2.45, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.45)
        self.at("physiology")
        phys = chip("physiology", GREY, 30).next_to(q, RIGHT, buff=0.5)
        self.play(FadeIn(phys, shift=LEFT * 0.2), run_time=0.45)
        self.at("hand waved")
        hw = T("only hand-waved at", 30, GREY).next_to(phys, RIGHT, buff=0.5)
        wig = FunctionGraph(lambda x: 0.09 * np.sin(11 * x), x_range=[-hw.width / 2, hw.width / 2],
                            color=GREY, stroke_width=4).next_to(hw, DOWN, buff=0.12)
        self.play(FadeIn(hw, shift=LEFT * 0.2), Create(wig), run_time=0.8)

        # --- where the lactate of a sprinting muscle goes
        self.at("where the", lead=0.3)
        self.play(FadeOut(Group(hw, wig)), q.animate.scale(0.5).move_to([5.55, 1.15, 0]), run_time=0.01)
        self.remove(q); self.add(q)
        self.play(FadeOut(phys), FadeOut(q), run_time=0.35)
        self.at("lactate")
        lac = self.chip_at("lactate", AMBER, 3.0, 0.9, 32)
        self.play(FadeIn(lac, scale=0.85), run_time=0.45)
        self.at("sprinting")
        mus = chip("sprinting muscle", RED, 32).move_to([-0.6, 0.9, 0])
        self.play(FadeIn(mus, shift=RIGHT * 0.2), run_time=0.45)
        a1 = Arrow(mus.get_right() + RIGHT * 0.08, lac.get_left() + LEFT * 0.08, buff=0, color=GREY, stroke_width=4,
                   max_tip_length_to_length_ratio=0.3)
        self.play(GrowArrow(a1), run_time=0.35)
        self.at("goes")
        a2 = DashedLine(lac.get_right() + RIGHT * 0.1, [5.2, 0.9, 0], color=GOLD, stroke_width=5)
        a2.add_tip(tip_length=0.2)
        q2 = T("?", 80, GOLD, font=TITLE_FONT).move_to([5.75, 0.9, 0])
        self.play(Create(a2), FadeIn(q2, scale=0.6), run_time=0.6)

        # --- where its next push of fuel comes from
        self.at("where", nth=1, lead=0.25)
        fuel = chip("next push of fuel", GREEN, 32).move_to([-0.6, -1.0, 0])
        self.play(FadeIn(fuel, shift=UP * 0.1), run_time=0.5)
        self.at("push of fuel", lead=0.1)
        a3 = DashedLine(fuel.get_top() + UP * 0.08, mus.get_bottom() + DOWN * 0.08, color=GOLD, stroke_width=5)
        a3.add_tip(tip_length=0.2)
        self.play(Create(a3), run_time=0.5)
        self.at("comes")
        q3 = T("?", 80, GOLD, font=TITLE_FONT).move_to([0.5, -0.05, 0])
        self.play(FadeIn(q3, scale=0.6), run_time=0.45)

        # --- by measuring sugar quantitatively through the whole living animal
        self.at("by measuring", lead=0.45)
        self.play(FadeOut(Group(lac, mus, a1, a2, q2, fuel, a3, q3)), run_time=0.25)
        xs = [-0.5, 2.0, 4.5]
        names = [("muscle", RED), ("blood", GREY), ("liver", BLUE)]
        cards = VGroup(*[chip(n, c, 28).move_to([x, 1.45, 0]) for (n, c), x in zip(names, xs)])
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in cards], lag_ratio=0.2), run_time=0.5)
        # sugar followed through every compartment (no amounts shown: the entry gives none)
        self.at("sugar", lead=0.1)
        TY = 0.35
        track = Line([xs[0], TY, 0], [xs[-1], TY, 0], color=GREEN, stroke_width=4)
        nodes = VGroup(*[Dot([x, TY, 0], radius=0.13, color=GREEN) for x in xs])
        sugar = T("sugar", 28, GREEN).move_to([(xs[0] + xs[1]) / 2, TY - 0.45, 0])
        self.play(Create(track), LaggedStart(*[FadeIn(d, scale=0.5) for d in nodes], lag_ratio=0.3),
                  FadeIn(sugar), run_time=0.45)
        # --- quantitatively: one measuring scale under the whole path, read at every compartment
        self.at("quantitatively", lead=0.15)
        RY = -1.15
        rule = Line([-1.0, RY, 0], [5.0, RY, 0], color=TEXT, stroke_width=3)
        ticks = VGroup(*[Line([-1.0 + 0.3 * i, RY, 0], [-1.0 + 0.3 * i, RY + (0.28 if i % 5 == 0 else 0.15), 0],
                              color=TEXT, stroke_width=3) for i in range(21)])
        reads = VGroup(*[DashedLine([x, TY - 0.15, 0], [x, RY + 0.32, 0], color=GREEN, stroke_width=3,
                                    dash_length=0.08) for x in xs])
        self.play(Create(rule), LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.05),
                  LaggedStart(*[Create(r) for r in reads], lag_ratio=0.3), run_time=0.45)
        self.at("whole living animal", lead=0.5)
        outer = DashedVMobject(RoundedRectangle(corner_radius=0.3, width=7.4, height=4.6, stroke_color=GOLD, stroke_width=3),
                               num_dashes=70, dashed_ratio=0.6).move_to([CX, -0.05, 0])
        lbl = T("the whole living animal", 28, GOLD, font=TITLE_FONT).move_to([CX, 2.75, 0])
        self.play(Create(outer), FadeIn(lbl, shift=UP * 0.1), run_time=0.9)
        self.finish()


class S02Circuit(BioScene):
    def construct(self):
        self.add_column("both")
        self.at("circuit")
        circ = T("a circuit", 40, GOLD, font=TITLE_FONT).move_to([CX, 2.85, 0])
        self.play(FadeIn(circ, shift=DOWN * 0.1), run_time=0.5)

        self.at("muscle")
        mus = box("muscle", RED, MX)
        self.play(FadeIn(mus, scale=0.95), run_time=0.45)
        self.at("glucose")
        glu = self.chip_at("glucose", GREEN, MX, -0.35, 26)
        self.play(FadeIn(glu, scale=0.85), run_time=0.4)
        self.at("lactate")
        lac = self.chip_at("lactate", AMBER, MX, -0.35, 26)
        self.play(ReplacementTransform(glu, lac), run_time=0.5)

        self.at("the blood carries")
        top = arrow(TOP_Y, True)
        blood = T("blood", 26, GREY).move_to([(MX + LX) / 2, 0, 0])
        self.play(GrowArrow(top), FadeIn(blood), lac.animate.move_to([(MX + LX) / 2, 1.35, 0]), run_time=1.1)
        self.at("to the liver", lead=0.1)
        liv = box("liver", BLUE, LX)
        lac_in = lac.copy()   # the label stays on the outbound arrow; a copy enters the liver
        self.play(FadeIn(liv, scale=0.95), lac_in.animate.move_to([LX, -0.35, 0]), run_time=0.9)

        self.at("rebuilds")
        glu2 = self.chip_at("glucose", GREEN, LX, -0.35, 26)
        self.play(ReplacementTransform(lac_in, glu2), run_time=0.6)
        self.at("sends", lead=0.1)
        bot = arrow(BOT_Y, False)
        glu_lbl = glu2.copy()
        self.play(GrowArrow(bot), glu_lbl.animate.move_to([(MX + LX) / 2, -1.35, 0]),
                  glu2.animate.move_to([(MX + LX) / 2, -1.35, 0]), run_time=0.8)
        # one copy delivers the glucose back into the muscle; the label stays on the return arrow
        self.play(glu2.animate.move_to([MX, -0.35, 0]).set_opacity(0), run_time=0.7)
        self.remove(glu2)
        self.finish()


class S03Draw(BioScene):
    def construct(self):
        self.add_column("both")
        mus, liv, top, bot, blood, lac, glu = self.static_loop()
        circ = T("a circuit", 40, GOLD, font=TITLE_FONT).move_to([CX, 2.85, 0])
        self.add(circ)
        self.at("first")
        first = T("the first inter-organ cycle", 40, GOLD, font=TITLE_FONT).move_to([CX, 2.85, 0])
        self.play(ReplacementTransform(circ, first), run_time=0.5)
        self.at("inter organ", lead=0.0)
        self.play(Indicate(mus, color=GOLD, scale_factor=1.05), Indicate(liv, color=GOLD, scale_factor=1.05), run_time=0.9)
        self.at("fuel economy", lead=0.6)
        eco = T("the body’s fuel economy", 32, TEXT, font=TITLE_FONT).move_to([CX, -2.7, 0])
        self.play(FadeIn(eco, shift=UP * 0.1), run_time=0.5)
        self.at("you could draw", lead=0.25)
        path = RoundedRectangle(corner_radius=0.5, width=8.1, height=3.9, color=GOLD, stroke_width=6)
        path.move_to([CX - 0.05, 0, 0])
        pen = Dot(radius=0.14, color=GOLD).move_to(path.get_start())
        self.play(Create(path, rate_func=linear), MoveAlongPath(pen, path, rate_func=linear), run_time=1.3)
        self.play(FadeOut(pen), run_time=0.2)
        self.finish()


class S04Loop(BioScene):
    """Silent recap: the contribution as a circulating loop."""
    def construct(self):
        self.add_column("both")
        mus, liv, top, bot, blood, lac, glu = self.static_loop()
        head = T("Fuel is traded between tissues,", 40, GOLD, font=TITLE_FONT).move_to([CX, 2.85, 0])
        fit(head, max_w=8.6)
        tail = T("not just burned where it sits.", 36, GREY, font=TITLE_FONT).move_to([CX, -2.7, 0])
        self.play(FadeIn(head, shift=DOWN * 0.1), run_time=0.8)
        xa, xb = MX + BW / 2 + 0.05, LX - BW / 2 - 0.05
        for lap in range(3):
            d1 = Dot(radius=0.17, color=AMBER).move_to([xa, TOP_Y, 0]).set_z_index(5)
            self.play(FadeIn(d1, run_time=0.2))
            self.play(d1.animate.move_to([xb, TOP_Y, 0]), run_time=1.3, rate_func=linear)
            self.play(FadeOut(d1, run_time=0.15), Indicate(liv[0], color=BLUE, scale_factor=1.04), run_time=0.5)
            d2 = Dot(radius=0.17, color=GREEN).move_to([xb, BOT_Y, 0]).set_z_index(5)
            self.play(FadeIn(d2, run_time=0.2))
            self.play(d2.animate.move_to([xa, BOT_Y, 0]), run_time=1.3, rate_func=linear)
            self.play(FadeOut(d2, run_time=0.15), Indicate(mus[0], color=RED, scale_factor=1.04), run_time=0.5)
            if lap == 0:
                self.play(FadeIn(tail, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S05Nobel(BioScene):
    def construct(self):
        self.add_column("both")
        self.play(*self.focus("right"), run_time=0.4)
        name = T("Gerty Cori", 46, GOLD, font=TITLE_FONT).move_to([CX, 2.3, 0])
        self.play(FadeIn(name, shift=DOWN * 0.1), run_time=0.4)
        self.at("first woman", lead=0.25)
        fw = T("the first woman", 40, TEXT, font=TITLE_FONT).move_to([CX, 0.85, 0])
        self.play(FadeIn(fw, shift=UP * 0.1), run_time=0.45)
        self.at("Nobel", lead=0.3)
        medal = VGroup(Circle(radius=0.8, color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.2),
                       T("Nobel", 28, GOLD, weight=BOLD)).move_to([-0.1, -1.5, 0])
        lab = VGroup(T("Nobel Prize", 34, GOLD, font=TITLE_FONT), T("in Medicine", 34, GOLD, font=TITLE_FONT)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.6, -1.5, 0])
        self.play(GrowFromCenter(medal), FadeIn(lab, shift=LEFT * 0.2), run_time=0.7)
        self.finish()


class S06Quote(BioScene):
    def construct(self):
        self.add_column("both")
        lines = [T("Our efforts have been largely complementary,", 34, TEXT, font=TITLE_FONT),
                 T("and one without the other would not have", 34, TEXT, font=TITLE_FONT),
                 T("gone as far as in combination.”", 34, TEXT, font=TITLE_FONT)]
        qg = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        fit(qg, max_w=8.0)
        qg.move_to([CX + 0.1, 0.5, 0])
        mark = T("“", 100, GOLD, font=TITLE_FONT).scale(0.7).next_to(lines[0], LEFT, buff=0.12)
        mark.align_to(lines[0], UP).shift(UP * 0.12)
        att = T("Carl & Gerty Cori", 30, GOLD).next_to(qg, DOWN, buff=0.6).align_to(qg, RIGHT)
        self.play(FadeIn(mark, shift=DOWN * 0.1), run_time=0.6)
        for ln in lines:
            self.play(FadeIn(ln, shift=UP * 0.1), run_time=1.0)
            self.wait(0.6)
        self.play(FadeIn(att, shift=UP * 0.1), run_time=0.7)
        self.finish()


class S07End(BioScene):
    def construct(self):
        img, border = portrait(height=2.3, center=(0, 2.0))
        cap = T(CAPTION, 22, GREY).move_to([0, 2.0 - 1.15 - 0.3, 0])
        line = T("Mapped the first inter-organ fuel loop:", 38, font=TITLE_FONT)
        line2 = T("muscle lactate to liver glucose.", 38, font=TITLE_FONT)
        lg = VGroup(line, line2).arrange(DOWN, buff=0.2).move_to([0, -0.55, 0])
        fit(lg, max_w=11.5)
        sub = T("biochemistrypedia.com", 24, TEAL).move_to([0, -1.85, 0])
        src = T("Source: The Molecule Hunters — the Coris profile", 22, GREY).move_to([0, -2.6, 0])
        self.play(FadeIn(img), FadeIn(border), FadeIn(cap), run_time=0.5)
        self.play(FadeIn(lg, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(sub), FadeIn(src), run_time=0.4)
        self.finish()
