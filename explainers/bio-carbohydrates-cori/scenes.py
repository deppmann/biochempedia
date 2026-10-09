"""Carl Cori & Gerty Cori: scientist profile video (Biochemistrypedia, carbohydrates lesson)

The portrait (public/scientists/cori.png, an AI-generated engraving-style illustration from
The Molecule Hunters) is the anchor: the title scene pushes in on it, then it stays as a framed
inset on the left while the right side animates the story's beats as the narrator reaches them.
It is a two-person portrait, so the half of the picture the narration is about stays lit and the
other half is dimmed (Gerty in the exam and refusal beats, Carl when he insists the prize was
hers, both when the story says "they").
Every cue is a self.at("spoken words") lookup in audio/words.json (word timestamps of the real
audio). Nothing on screen adds a fact that is not in the lesson entry (name, dates, contribution,
story, quotes).

COLOR MAP (one color per concept, whole video)
  GOLD   = the Coris, the portrait frame, recognition (refusal, Nobel, "as much hers", first woman)
  YELLOW = years and numbers (eight years, five, one year, 1947)
  TEAL   = people in roles and institutions (refinery manager, institute director, this chapter)
  RED    = obstacles (the exam built to keep women out, the director's order, "not how things were done")
  BLUE   = the enzyme (glycogen phosphorylase)
  GREEN  = glycogen, glucose-1-phosphate, glucose, the molecules taken apart
  AMBER  = lactate
  PURPLE = muscle and liver
  GREY   = structure, labels
"""
import os
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

config.disable_caching = True

AMBER = "#E0A458"
PURPLE = "#A78BFA"
CX = 2.0            # centre of the content area to the right of the portrait column
PORT_X = -4.5       # portrait column centre
PORT_H = 3.375
PORT_Y = 1.3
IMG = Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent / "cori_crop.png"
NAME = "Carl Cori & Gerty Cori"
DATES = "Carl 1896–1984 · Gerty 1896–1957"
CAPTION = "illustration · AI-generated"
DIM = 0.68


def portrait(height=PORT_H, center=(PORT_X, PORT_Y)):
    img = ImageMobject(str(IMG))
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["cubic"])
    img.set_height(height)
    img.move_to([center[0], center[1], 0])
    border = Rectangle(width=img.width, height=img.height, stroke_color=GOLD, stroke_width=3, fill_opacity=0)
    border.move_to(img)
    return img, border


class BioScene(SpokenScene):
    """Adds the portrait column with a lit/dimmed half (focus 'C' Carl, 'G' Gerty, 'B' both)."""

    def add_column(self, focus="B", show=True):
        img, border = portrait()
        w, h = img.width, img.height
        cx, cy = PORT_X, PORT_Y
        self.ovL = Rectangle(width=w / 2, height=h, stroke_width=0, fill_color=BG, fill_opacity=0)
        self.ovR = self.ovL.copy()
        self.ovL.move_to([cx - w / 4, cy, 0]); self.ovR.move_to([cx + w / 4, cy, 0])
        self.hfL = Rectangle(width=w / 2, height=h, stroke_color=GOLD, stroke_width=5, fill_opacity=0).move_to(self.ovL)
        self.hfR = Rectangle(width=w / 2, height=h, stroke_color=GOLD, stroke_width=5, fill_opacity=0).move_to(self.ovR)
        self.hfL.set_stroke(opacity=0); self.hfR.set_stroke(opacity=0)
        by = cy - h / 2 - 0.34
        self.nL = T("Carl Cori", 26, TEXT, font=TITLE_FONT).move_to([cx - w / 4, by, 0])
        self.nR = T("Gerty Cori", 26, TEXT, font=TITLE_FONT).move_to([cx + w / 4, by, 0])
        self.nR.align_to(self.nL, UP)
        self.dL = T("1896–1984", 22, GOLD).move_to([cx - w / 4, by - 0.42, 0])
        self.dR = T("1896–1957", 22, GOLD).move_to([cx + w / 4, by - 0.42, 0])
        self.cap = T(CAPTION, 22, GREY).move_to([cx, by - 0.95, 0])
        self._apply_focus(focus)
        if show:
            self.add(img, self.ovL, self.ovR, border, self.hfL, self.hfR, self.nL, self.nR, self.dL, self.dR, self.cap)

    def _state(self, f):
        return dict(ovL=DIM if f == "G" else 0, ovR=DIM if f == "C" else 0,
                    hfL=1 if f == "C" else 0, hfR=1 if f == "G" else 0,
                    cL=GREY if f == "G" else TEXT, cR=GREY if f == "C" else TEXT)

    def _apply_focus(self, f):
        s = self._state(f)
        self.ovL.set_fill(BG, s["ovL"]); self.ovR.set_fill(BG, s["ovR"])
        self.hfL.set_stroke(opacity=s["hfL"]); self.hfR.set_stroke(opacity=s["hfR"])
        self.nL.set_color(s["cL"]); self.nR.set_color(s["cR"])

    def focus(self, f):
        """Animations that move the light to Carl ('C'), Gerty ('G') or both ('B')."""
        s = self._state(f)
        return [self.ovL.animate.set_fill(BG, s["ovL"]), self.ovR.animate.set_fill(BG, s["ovR"]),
                self.hfL.animate.set_stroke(opacity=s["hfL"]), self.hfR.animate.set_stroke(opacity=s["hfR"]),
                self.nL.animate.set_color(s["cL"]), self.nR.animate.set_color(s["cR"])]

    def until(self, t, lead=0.2):
        rest = t - lead - self.elapsed()
        if rest > 0.02:
            self.wait(rest)

    def chip_at(self, text, color, x, y, size=28, **kw):
        c = chip(text, color, size, **kw)
        c.move_to([x, y, 0])
        return c


class S00Title(BioScene):
    def construct(self):
        brand = T("BIOCHEMISTRYPEDIA  ·  SCIENTIST PROFILE", 22, TEAL, weight=BOLD).move_to([0, 3.4, 0])
        img, border = portrait()
        big_h = 4.1
        k = big_h / PORT_H
        big_c = np.array([0.0, 0.85, 0.0])
        for m in (img, border):
            m.scale(k, about_point=ORIGIN).move_to(big_c)
        cap = T(CAPTION, 22, GREY).move_to([0, 0.85 - big_h / 2 - 0.3, 0])
        name = T(NAME, 52, font=TITLE_FONT)
        fit(name, max_w=11.5)
        name.move_to([0, -2.55, 0])
        dates = T(DATES, 28, GOLD).move_to([0, -3.3, 0])
        rule = Line(LEFT * 1.0, RIGHT * 1.0, color=GOLD, stroke_width=4).move_to([0, -2.95, 0])

        self.play(FadeIn(img), FadeIn(border), FadeIn(brand), FadeIn(cap), run_time=0.4)
        # slow push-in while the name and dates arrive
        self.play(img.animate.scale(1.05), border.animate.scale(1.05),
                  Write(name, run_time=1.0), run_time=1.5, rate_func=linear)
        self.play(GrowFromCenter(rule), FadeIn(dates), run_time=0.35)

        # hand over to the inset layout used by every later scene
        self.add_column("B", show=False)
        inset_cap_pos = self.cap.get_center()
        for m in (self.nL, self.nR, self.dL, self.dR):
            m.set_opacity(0)
        self.add(self.nL, self.nR, self.dL, self.dR)
        self.play(AnimationGroup(
            img.animate.scale(1 / (k * 1.05)).move_to([PORT_X, PORT_Y, 0]),
            border.animate.scale(1 / (k * 1.05)).move_to([PORT_X, PORT_Y, 0]),
            cap.animate.move_to(inset_cap_pos),
            Succession(AnimationGroup(FadeOut(name), FadeOut(dates), FadeOut(rule), FadeOut(brand)),
                       AnimationGroup(*[m.animate.set_opacity(1) for m in (self.nL, self.nR, self.dL, self.dR)])),
            run_time=0.8))
        self.finish()


class S01Exam(BioScene):
    def construct(self):
        self.add_column("B")
        self.play(*self.focus("G"), run_time=0.5)

        self.at("daughter of")
        dau = T("daughter of", 26, GREY).move_to([-0.1, 2.85, 0])
        self.play(FadeIn(dau, shift=RIGHT * 0.1), run_time=0.4)
        self.at("sugar refinery")
        mgr = self.chip_at("sugar-refinery manager", TEAL, 3.95, 2.85, 26)
        self.play(FadeIn(mgr, shift=LEFT * 0.15), run_time=0.5)
        self.at("an irony")
        irony = T("an irony she savored", 30, GOLD, font=TITLE_FONT).move_to([3.4, 1.9, 0])
        self.play(FadeIn(irony, shift=UP * 0.1), run_time=0.6)
        self.at("savored", lead=0.1)
        self.play(Indicate(irony, color=GOLD, scale_factor=1.08), run_time=0.7)

        # eight years of Latin, five of science
        self.at("she compressed", lead=0.0)
        self.at("eight years")
        sq = lambda: Square(0.4, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9)
        row1 = VGroup(*[sq() for _ in range(8)]).arrange(RIGHT, buff=0.12).move_to([-0.15, 0.75, 0])
        row1.align_to([-2.0, 0, 0], LEFT)
        lat = T("8 years of Latin", 26, YELLOW).move_to([4.2, 0.75, 0]).align_to([3.0, 0, 0], LEFT)
        self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in row1], lag_ratio=0.12), FadeIn(lat), run_time=1.1)
        self.at("five of")
        row2 = VGroup(*[sq() for _ in range(5)]).arrange(RIGHT, buff=0.12).move_to([0, 0.05, 0])
        row2.move_to([0, 0.05, 0]).align_to(row1, LEFT)
        sci = T("5 years of science", 26, YELLOW).move_to([4.2, 0.05, 0]).align_to(lat, LEFT)
        self.play(LaggedStart(*[FadeIn(b, scale=0.5) for b in row2], lag_ratio=0.12), FadeIn(sci), run_time=0.9)

        # compressed into a single year
        self.at("into a single year")
        one = self.chip_at("1 year", YELLOW, 0.2, -1.2, 32)
        self.play(ReplacementTransform(VGroup(row1, row2), one), FadeOut(VGroup(lat, sci)), run_time=1.0)

        # the exam built to keep women out
        self.at("to pass", lead=0.15)
        exam = self.chip_at("entrance exam", RED, 4.3, -1.2, 28)
        arr = Arrow(one.get_right() + RIGHT * 0.1, exam.get_left() + LEFT * 0.1, buff=0, color=GREY, stroke_width=5,
                    max_tip_length_to_length_ratio=0.3)
        self.play(GrowArrow(arr), run_time=0.4)
        self.at("entrance exam")
        self.play(FadeIn(exam, shift=LEFT * 0.15), run_time=0.5)
        self.at("built to keep women")
        keep = T("built to keep women out", 28, RED).move_to([4.0, -2.3, 0])
        self.play(FadeIn(keep, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S02Refusal(BioScene):
    def construct(self):
        self.add_column("G")

        # --- the director's order, and the refusal
        self.at("director")
        dirc = self.chip_at("institute director", TEAL, CX, 2.9, 30)
        self.play(FadeIn(dirc, shift=DOWN * 0.1), run_time=0.5)
        self.at("stop publishing")
        order = T("stop publishing with her husband", 30, RED).move_to([CX, 1.62, 0])
        down = Arrow(dirc.get_bottom() + DOWN * 0.05, order.get_top() + UP * 0.12, buff=0, color=RED, stroke_width=4,
                     max_tip_length_to_length_ratio=0.35)
        self.play(GrowArrow(down), FadeIn(order, shift=DOWN * 0.1), run_time=0.7)
        self.at("two married people")
        carl = VGroup(Circle(radius=0.4, color=GOLD, fill_color=GOLD, fill_opacity=0.25, stroke_width=4),
                      T("Carl", 24, GOLD)).arrange(DOWN, buff=0.15)
        gerty = VGroup(Circle(radius=0.4, color=GOLD, fill_color=GOLD, fill_opacity=0.25, stroke_width=4),
                       T("Gerty", 24, GOLD)).arrange(DOWN, buff=0.15)
        carl.move_to([0.6, 0.25, 0]); gerty.move_to([3.4, 0.25, 0])
        gerty[1].align_to(carl[1], UP); gerty[0].align_to(carl[0], UP)
        self.play(FadeIn(carl, shift=RIGHT * 0.3), FadeIn(gerty, shift=LEFT * 0.3), run_time=0.5)
        self.at("a byline")
        br = Brace(VGroup(carl, gerty), DOWN, buff=0.12, color=GOLD)
        bl = T("a shared byline", 26, GOLD).next_to(br, DOWN, buff=0.1)
        self.play(GrowFromCenter(br), FadeIn(bl), run_time=0.5)
        self.at("not how things")
        nope = T("not how things were done", 28, RED).move_to([CX, -1.85, 0])
        self.play(FadeIn(nope, shift=UP * 0.1), run_time=0.5)
        self.at("she refused")
        strike = Line(order.get_left() + LEFT * 0.1, order.get_right() + RIGHT * 0.1, color=GOLD, stroke_width=6)
        refused = T("She refused.", 38, GOLD, font=TITLE_FONT).move_to([CX, -2.9, 0])
        self.play(Create(strike), run_time=0.35)
        self.play(FadeIn(refused, shift=UP * 0.1), run_time=0.4)

        # --- out of the refusal: how glycogen is stored and mobilized
        self.at("out of that", lead=0.45)
        ref = self.chip_at("that refusal", GOLD, CX, 3.0, 28)
        self.play(FadeOut(Group(dirc, down, order, strike, carl, gerty, br, bl, nope, refused)), run_time=0.35)
        self.at("refusal", lead=0.45)
        self.play(FadeIn(ref, shift=DOWN * 0.1), run_time=0.45)
        self.at("came the work", lead=0.1)
        a1 = Arrow([CX, 2.6, 0], [CX, 2.05, 0], buff=0, color=GREY, stroke_width=5, max_tip_length_to_length_ratio=0.35)
        came = T("came the work", 26, GREY).move_to([CX + 1.55, 2.33, 0])
        self.play(GrowArrow(a1), FadeIn(came), *self.focus("B"), run_time=0.6)
        self.at("glycogen")
        gly = self.chip_at("glycogen", GREEN, CX, 1.4, 30)
        self.play(FadeIn(gly, scale=0.9), run_time=0.5)
        self.at("stored and", lead=0.1)
        ain = Arrow([CX - 3.0, 1.4, 0], [CX - 1.3, 1.4, 0], buff=0, color=GREEN, stroke_width=5, max_tip_length_to_length_ratio=0.3)
        stored = T("stored", 26, GREEN).move_to([CX - 2.15, 0.85, 0])
        self.play(GrowArrow(ain), FadeIn(stored), run_time=0.5)
        self.until(12.2, lead=0.2)
        aout = Arrow([CX + 1.3, 1.4, 0], [CX + 3.0, 1.4, 0], buff=0, color=GREEN, stroke_width=5, max_tip_length_to_length_ratio=0.3)
        mob = T("mobilized", 26, GREEN).move_to([CX + 2.15, 0.85, 0])
        self.play(GrowArrow(aout), FadeIn(mob), run_time=0.5)

        # --- the three pieces of the work
        self.until(13.86, lead=0.7)
        self.play(FadeOut(Group(ref, a1, came, gly, ain, stored, aout, mob)), run_time=0.4)
        self.at("phosphorylase", lead=0.2)
        enz = self.chip_at("glycogen phosphorylase", BLUE, CX, 2.9, 30)
        self.play(FadeIn(enz, shift=UP * 0.1), run_time=0.6)
        self.at("glucose", lead=0.25)
        g1p = self.chip_at("glucose-1-phosphate", GREEN, CX - 2.2, 1.5, 26)
        self.play(FadeIn(g1p, shift=UP * 0.1), run_time=0.6)
        self.at("Cory ester")
        cori = T("“Cori ester”", 34, GOLD, font=TITLE_FONT).move_to([CX + 3.0, 1.5, 0])
        link = Line(g1p.get_right() + RIGHT * 0.1, cori.get_left() + LEFT * 0.1, color=GOLD, stroke_width=3)
        self.play(Create(link), FadeIn(cori, shift=LEFT * 0.1), run_time=0.5)

        self.at("the Cory cycle", lead=0.3)
        title = T("the Cori cycle", 34, GOLD, font=TITLE_FONT).move_to([CX, 0.3, 0])
        mus = self.chip_at("muscle", PURPLE, CX - 2.8, -1.5, 28)
        liv = self.chip_at("liver", PURPLE, CX + 2.8, -1.5, 28)
        self.play(FadeIn(title, shift=UP * 0.1), FadeIn(mus), FadeIn(liv), run_time=0.7)
        self.at("lactate")
        top = Arrow([mus.get_right()[0] + 0.1, -1.2, 0], [liv.get_left()[0] - 0.1, -1.2, 0], buff=0, color=AMBER,
                    stroke_width=5, max_tip_length_to_length_ratio=0.25)
        lact = T("lactate", 26, AMBER).move_to([CX + 0.05, -0.8, 0])
        self.play(GrowArrow(top), FadeIn(lact), run_time=0.5)
        self.at("muscle")
        self.play(Indicate(mus, color=PURPLE, scale_factor=1.08), run_time=0.45)
        self.at("liver")
        self.play(Indicate(liv, color=PURPLE, scale_factor=1.08), run_time=0.45)
        self.at("glucose", nth=1)
        bot = Arrow([liv.get_left()[0] - 0.1, -1.8, 0], [mus.get_right()[0] + 0.1, -1.8, 0], buff=0, color=GREEN,
                    stroke_width=5, max_tip_length_to_length_ratio=0.25)
        glu = T("glucose", 26, GREEN).move_to([CX + 0.05, -2.25, 0])
        self.play(GrowArrow(bot), FadeIn(glu), run_time=0.5)
        self.finish()


class S03Nobel(BioScene):
    def construct(self):
        self.add_column("B")
        self.at("the 1947 Nobel", lead=0.0)
        medal = VGroup(Circle(radius=0.68, color=GOLD, stroke_width=5, fill_color=GOLD, fill_opacity=0.2),
                       T("Nobel", 24, GOLD, weight=BOLD)).move_to([CX - 1.3, 2.6, 0])
        yr = M("1947", 60, YELLOW).move_to([CX + 1.5, 2.6, 0])
        self.play(Write(yr), run_time=0.5)
        self.play(GrowFromCenter(medal), run_time=0.5)
        self.at("arrived", lead=0.1)
        self.play(Indicate(medal, color=GOLD, scale_factor=1.12), run_time=0.7)

        self.at("insisted", lead=0.5)
        self.play(*self.focus("C"), run_time=0.5)
        ins = T("Carl insisted", 30, TEXT, font=TITLE_FONT).move_to([CX, 1.35, 0])
        self.play(FadeIn(ins, shift=UP * 0.1), run_time=0.4)
        self.at("the prize was")
        x0, full = CX - 2.0, 4.6
        lab_c = T("Carl", 26, GREY).move_to([x0 - 0.75, 0.55, 0])
        lab_g = T("Gerty", 26, GOLD).move_to([x0 - 0.75, -0.25, 0])
        bar_c = Rectangle(width=full, height=0.5, stroke_width=0, fill_color=GREY, fill_opacity=0.85).move_to([x0 + full / 2, 0.55, 0])
        self.play(FadeIn(lab_c), GrowFromEdge(bar_c, LEFT), FadeIn(lab_g), run_time=0.5)
        self.at("as much hers")
        bar_g = Rectangle(width=full, height=0.5, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to([x0 + full / 2, -0.25, 0])
        eq = T("as much hers", 34, GOLD, font=TITLE_FONT).move_to([CX, -1.2, 0])
        self.play(GrowFromEdge(bar_g, LEFT), FadeIn(eq, shift=UP * 0.1), run_time=0.8)

        self.at("and Gertie became", lead=0.3)
        self.play(FadeOut(Group(ins, lab_c, lab_g, bar_c, bar_g, eq)), *self.focus("G"), run_time=0.45)
        self.at("first woman", lead=0.2)
        first = T("the first woman", 44, GOLD, font=TITLE_FONT).move_to([CX, 0.6, 0])
        self.play(FadeIn(first, shift=UP * 0.15), run_time=0.6)
        self.at("Nobel in medicine", lead=0.25)
        prize = self.chip_at("to win the Nobel in Medicine", GOLD, CX, -0.8, 30)
        self.play(FadeIn(prize, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S04Career(BioScene):
    def construct(self):
        self.add_column("G")
        bp = self.chip_at("glycogen branch points", GREEN, CX, 2.55, 30)
        self.play(FadeIn(bp, shift=UP * 0.1), *self.focus("B"), run_time=0.5)
        self.at("non reducing")
        nr = self.chip_at("non-reducing ends", GREEN, CX, 1.35, 30)
        self.play(FadeIn(nr, shift=UP * 0.1), run_time=0.5)
        self.at("in this chapter")
        chap = T("in this chapter", 28, TEAL).move_to([CX, 0.45, 0])
        self.play(FadeIn(chap, shift=UP * 0.1), run_time=0.5)

        self.at("they spent")
        carl = VGroup(Circle(radius=0.4, color=GOLD, fill_color=GOLD, fill_opacity=0.25, stroke_width=4),
                      T("Carl", 24, GOLD)).arrange(DOWN, buff=0.15).move_to([0.6, -1.5, 0])
        gerty = VGroup(Circle(radius=0.4, color=GOLD, fill_color=GOLD, fill_opacity=0.25, stroke_width=4),
                       T("Gerty", 24, GOLD)).arrange(DOWN, buff=0.15).move_to([3.4, -1.5, 0])
        gerty[1].align_to(carl[1], UP); gerty[0].align_to(carl[0], UP)
        self.play(FadeIn(carl, shift=RIGHT * 0.2), FadeIn(gerty, shift=LEFT * 0.2), run_time=0.5)
        self.at("career")
        career = T("a career", 38, GOLD, font=TITLE_FONT).move_to([CX, -2.95, 0])
        self.play(FadeIn(career, shift=UP * 0.1), run_time=0.5)
        self.at("taking apart")
        pieces = []
        anims = []
        for c in (bp, nr):
            box, label = c[0], c[1]
            dashed = DashedVMobject(box.copy(), num_dashes=44, dashed_ratio=0.55).set_color(GREEN)
            anims += [FadeOut(box), FadeIn(dashed)]
            pieces.append(dashed)
            anims += [label.animate.shift(RIGHT * 0.0)]
        self.play(*anims, run_time=0.3)
        self.play(pieces[0].animate.shift(LEFT * 0.35 + UP * 0.05), pieces[1].animate.shift(RIGHT * 0.35 + DOWN * 0.05),
                  bp[1].animate.shift(LEFT * 0.35 + UP * 0.05), nr[1].animate.shift(RIGHT * 0.35 + DOWN * 0.05),
                  run_time=0.8)
        self.finish()


class S05Quote(BioScene):
    def construct(self):
        self.add_column("B")
        self.play(*self.focus("C"), run_time=0.5)
        lines = [T("“That the award should have included", 36, TEXT, font=TITLE_FONT),
                 T("my wife as well has been a source", 36, TEXT, font=TITLE_FONT),
                 T("of deep satisfaction to me.”", 36, TEXT, font=TITLE_FONT)]
        qg = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        for i, ln in enumerate(lines[1:], 1):
            ln.align_to(lines[0], UP).shift(DOWN * 0.68 * i)
        fit(qg, max_w=8.4)
        qg.move_to([CX + 0.1, 0.8, 0])
        att = T("Carl Cori", 30, GOLD).next_to(qg, DOWN, buff=0.6).align_to(qg, RIGHT)
        for ln in lines:
            self.play(FadeIn(ln, shift=UP * 0.1), run_time=0.9)
            self.wait(0.45)
        self.play(FadeIn(att, shift=UP * 0.1), run_time=0.6)
        self.finish()


class S06End(BioScene):
    def construct(self):
        img, border = portrait(height=2.3, center=(0, 2.0))
        cap = T(CAPTION, 22, GREY).move_to([0, 2.0 - 1.15 - 0.3, 0])
        l1 = T("Worked out glycogen enzyme by enzyme;", 38, font=TITLE_FONT)
        l2 = T("shared the 1947 Nobel Prize.", 38, font=TITLE_FONT)
        lg = VGroup(l1, l2).arrange(DOWN, buff=0.2).move_to([0, -0.55, 0])
        fit(lg, max_w=11.5)
        sub = T("biochemistrypedia.com", 24, TEAL).move_to([0, -1.85, 0])
        src = T("Source: The Molecule Hunters (v10) · the Cori partnership profile", 22, GREY).move_to([0, -2.6, 0])
        self.play(FadeIn(img), FadeIn(border), FadeIn(cap), run_time=0.5)
        self.play(FadeIn(lg, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(sub), FadeIn(src), run_time=0.4)
        self.finish()
