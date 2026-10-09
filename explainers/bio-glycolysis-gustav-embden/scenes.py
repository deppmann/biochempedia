"""Gustav Embden: a scientist profile (Biochemistrypedia, glycolysis lesson).

Narration is the lesson entry's `story`, verbatim. Everything on screen comes from that entry
(name, dates, contribution, story, quotes). The portrait (public/scientists/gustav-embden.png,
cropped to the figure as embden_crop.png) is an AI-generated engraving-style illustration from
The Molecule Hunters; it is captioned "illustration · AI-generated" whenever it is on screen at a
readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = Embden: his name/dates, his standard, his scheme, "the first correct map"
  YELLOW = years (twenty years, 1932, 1933)
  RED    = the consensus and what stood in the way: methylglyoxal theory, Neuberg and his grip,
           "contamination", the blocked route, the Nazis' harm
  BLUE   = what Embden found: the three-carbon molecule, phosphoglyceric acid, pyruvic acid
  GREEN  = sugar / glucose
  TEXT   = energy (plain white chip)
  PINK   = journals (the leading biochemical journal, the clinical journal)
  PLACE (lavender) = places: Frankfurt, Europe
  GREY   = structure, labels, de-emphasized things
No molecular structure is drawn: molecules appear only as labelled chips.
"""
import os
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

config.disable_caching = True

PORTRAIT = str(Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent / "embden_crop.png")
CAPTION = "illustration · AI-generated"
NAME = "Gustav Embden"
DATES = "1874–1933"
PLACE = "#B39DDB"
PINK = "#E58FB3"   # journals

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


def pop(mob):
    return FadeIn(mob, shift=UP * 0.12)


def arrow(a, b, color=GREY, w=4, tip=0.3):
    return Arrow(a, b, buff=0, color=color, stroke_width=w, max_tip_length_to_length_ratio=tip)


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


# ----------------------------------------------------------------------------- s01 the consensus
class S01Methylglyoxal(ProfileScene):
    def construct(self):
        self.add_inset()
        # twenty years: twenty blocks
        blocks = VGroup(*[Square(0.26, stroke_width=0, fill_color=YELLOW, fill_opacity=0.9) for _ in range(20)])
        blocks.arrange(RIGHT, buff=0.08).move_to([PANEL_C, 2.75, 0])
        yrs = T("twenty years", 28, YELLOW).next_to(blocks, UP, buff=0.22)
        self.at("20 years")
        self.play(FadeIn(yrs), LaggedStart(*[FadeIn(b, scale=0.5) for b in blocks], lag_ratio=0.08), run_time=1.2)

        # sugar -> methylglyoxal: the field's theory
        sugar = lab("sugar", GREEN, 30).move_to([-0.2, 1.1, 0])
        self.at("sugar broke down")
        self.play(pop(sugar), run_time=0.45)
        a1 = arrow(sugar.get_right() + RIGHT * 0.1, [2.3, 1.1, 0], GREY, 5)
        self.at("through a compound")
        self.play(GrowArrow(a1), run_time=0.5)
        mg = lab("methylglyoxal", RED, 30).move_to([4.3, 1.1, 0])
        self.at("methylglyoxal")
        self.play(pop(mg), run_time=0.45)

        brace = Brace(VGroup(sugar, mg), DOWN, buff=0.15, color=RED, stroke_width=2)
        theory = T("the field's theory", 28, RED).next_to(brace, DOWN, buff=0.12)
        self.at("the theory had")
        self.play(GrowFromCenter(brace), FadeIn(theory, shift=UP * 0.1), run_time=0.6)

        # the enforcer
        enf = lab("the enforcer", RED, 30).move_to([-0.5, -1.75, 0])
        self.at("an enforcer")
        self.play(pop(enf), run_time=0.45)
        neu = lab("Carl Neuberg", RED, 30).move_to([-0.5, -1.75, 0])
        self.at("Neuberg defended")
        self.play(ReplacementTransform(enf, neu), run_time=0.5)
        a2 = arrow([-0.5, -1.15, 0], [-0.5, -0.55, 0], RED, 4, 0.4)
        defended = T("defended it", 26, RED).next_to(a2, RIGHT, buff=0.15)
        self.play(GrowArrow(a2), FadeIn(defended), run_time=0.5)

        jr = lab(["leading biochemical", "journal"], PINK, 26).move_to([4.8, -1.75, 0])
        a3 = arrow(neu.get_right() + RIGHT * 0.1, jr.get_left() + LEFT * 0.1, PINK, 4, 0.3)
        edited = T("edited", 26, PINK).next_to(a3, UP, buff=0.12)
        self.at("also edited")
        self.play(GrowArrow(a3), FadeIn(edited), run_time=0.5)
        self.at("leading biochemical")
        self.play(pop(jr), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s02 Frankfurt
class S02Frankfurt(ProfileScene):
    def construct(self):
        self.add_inset()
        fr = lab("Frankfurt", PLACE, 30).move_to([-0.8, 2.75, 0])
        self.at("In Frankfurt")
        self.play(pop(fr), run_time=0.45)
        self.at("kept finding")
        a1 = arrow([0.4, 2.75, 0], [2.0, 2.75, 0], GREY, 4, 0.3)
        kf = T("kept finding", 24, GREY).next_to(a1, UP, buff=0.1)
        els = lab("something else", BLUE, 30).move_to([3.9, 2.75, 0])
        self.play(GrowArrow(a1), FadeIn(kf), run_time=0.5)
        self.play(pop(els), run_time=0.45)
        self.play(Indicate(els, color=BLUE, scale_factor=1.08), run_time=0.8)

        # his standard
        std = T("the standard he stated", 24, GREY).move_to([PANEL_C, 1.7, 0])
        self.at("standard he stated")
        self.play(FadeIn(std, shift=UP * 0.1), run_time=0.4)
        q1 = T("“meticulous cleanliness", 34, GOLD, font=TITLE_FONT).move_to([PANEL_C, 1.05, 0])
        q2 = T("and rigorous accuracy”", 34, GOLD, font=TITLE_FONT).move_to([PANEL_C, 0.45, 0])
        self.at("meticulous cleanliness")
        self.play(FadeIn(q1, shift=UP * 0.1), run_time=0.6)
        self.at("rigorous accuracy")
        self.play(FadeIn(q2, shift=UP * 0.1), run_time=0.6)

        # a three-carbon molecule, again and again
        mol = lab(["three-carbon", "molecule"], BLUE, 28).move_to([0.3, -0.95, 0])
        self.at("up a three")
        self.play(FadeOut(VGroup(std, q1, q2)), pop(mol), run_time=0.6)
        tally = VGroup(*[Line([0, -0.3, 0], [0, 0.3, 0], color=BLUE, stroke_width=6) for _ in range(3)])
        tally.arrange(RIGHT, buff=0.3).move_to([-0.1, -2.05, 0])
        again = T("again and again", 26, BLUE).next_to(tally, RIGHT, buff=0.4)
        self.at("again and again")
        self.play(Create(tally[0]), Flash(mol, color=BLUE, flash_radius=1.0, line_length=0.2), run_time=0.35)
        self.at("and again")
        self.play(Create(tally[1]), FadeIn(again), run_time=0.3)
        self.play(Create(tally[2]), run_time=0.3)

        # the consensus waves it off
        con = lab("consensus", RED, 30).move_to([5.0, -0.95, 0])
        self.at("and the consensus")
        self.play(pop(con), run_time=0.45)
        wave = arrow(con.get_left() + LEFT * 0.1, mol.get_right() + RIGHT * 0.1, RED, 4, 0.35)
        waved = T("waved off", 24, RED).next_to(wave, UP, buff=0.1)
        self.at("waving it off")
        self.play(GrowArrow(wave), FadeIn(waved), run_time=0.5)
        cont = lab("contamination", RED, 28).move_to([4.8, -2.35, 0])
        self.at("contamination")
        self.play(pop(cont), run_time=0.45)

        # trusted the molecule over the consensus: a balance
        pivot = np.array([PANEL_C, -1.0, 0.0])
        L = 2.6
        th = ValueTracker(0.0)
        end = lambda s: pivot + L * np.array([s * np.cos(th.get_value()), s * np.sin(th.get_value()), 0.0])  # s=-1 left
        beam = always_redraw(lambda: Line(end(-1), end(1), color=TEXT, stroke_width=7))
        foot = Polygon(pivot + np.array([0, -0.05, 0]), pivot + np.array([-0.5, -1.1, 0]), pivot + np.array([0.5, -1.1, 0]),
                       stroke_color=GREY, stroke_width=3, fill_color=GREY, fill_opacity=0.25)
        mol_off = UP * (mol.height / 2 + 0.06)
        con_off = UP * (con.height / 2 + 0.06)
        mol_lvl = end(-1) + mol_off
        con_lvl = end(1) + con_off
        self.at("Emden trusted", lead=1.0)
        self.play(FadeOut(VGroup(tally, again, wave, waved, cont, fr, a1, kf, els)),
                  mol.animate.move_to(mol_lvl), con.animate.move_to(con_lvl),
                  FadeIn(foot), Create(beam), run_time=0.7)
        mol.add_updater(lambda m: m.move_to(end(-1) + mol_off))
        con.add_updater(lambda m: m.move_to(end(1) + con_off))
        self.at("trusted the molecule")
        self.play(th.animate.set_value(0.2), run_time=1.2, rate_func=smooth)
        self.play(Indicate(mol, color=GOLD, scale_factor=1.06), run_time=0.6)
        mol.clear_updaters(); con.clear_updaters()
        self.finish()


# ----------------------------------------------------------------------------- s03 the map
class S03Map(ProfileScene):
    def construct(self):
        self.add_inset()
        yr = M("1932", 48, YELLOW).move_to([PANEL_C, 2.8, 0])
        self.at("In 1932")
        self.play(Write(yr), run_time=0.6)

        concl = T("his conclusion", 26, GOLD).move_to([PANEL_C, 2.0, 0])
        self.at("he concluded")
        self.play(FadeIn(concl, shift=UP * 0.1), run_time=0.4)

        # phosphoglyceric acid -> pyruvic acid
        pga = lab(["phosphoglyceric", "acid"], BLUE, 26).move_to([2.0, 0.8, 0])
        pyr = lab(["pyruvic", "acid"], BLUE, 26).move_to([5.45, 0.8, 0])
        a_pp = arrow(pga.get_right() + RIGHT * 0.08, pyr.get_left() + LEFT * 0.08, BLUE, 5, 0.35)
        self.at("phosphoglyceric acid")
        self.play(pop(pga), run_time=0.5)
        self.at("converted to")
        self.play(GrowArrow(a_pp), run_time=0.5)
        self.at("pyruvic acid")
        self.play(pop(pyr), run_time=0.5)

        # a unified scheme of glycolysis: glucose joins the chain
        glc = lab("glucose", GREEN, 26).move_to([-1.35, 0.8, 0])
        a_g = DashedLine(glc.get_right() + RIGHT * 0.08, pga.get_left() + LEFT * 0.08, color=GREY, stroke_width=4,
                         dash_length=0.12)
        a_g.add_tip(tip_length=0.2)
        self.at("laid out")
        self.play(pop(glc), Create(a_g), run_time=0.7)
        row = VGroup(glc, pga, pyr)
        brace = Brace(row, DOWN, buff=0.15, color=GOLD, stroke_width=2)
        scheme = T("a unified scheme of glycolysis", 28, GOLD).next_to(brace, DOWN, buff=0.12)
        self.at("unified scheme")
        self.play(GrowFromCenter(brace), FadeIn(scheme, shift=UP * 0.1), run_time=0.6)

        # compress the scheme to a chip; Neuberg's grip and the two journals
        sch = lab(["the", "scheme"], GOLD, 28).move_to([-0.1, -0.4, 0])
        self.at("to get around", lead=0.5)
        self.play(FadeOut(VGroup(glc, pga, pyr, a_pp, a_g, brace, scheme, concl)), pop(sch), run_time=0.7)
        grip = lab(["Neuberg's", "editorial grip"], RED, 26).move_to([4.55, 1.75, 0])
        self.at("editorial grip")
        self.play(pop(grip), run_time=0.5)

        biochem = lab(["biochemical", "journal"], PINK, 26).move_to([4.55, -0.15, 0])
        clin = lab(["clinical", "journal"], PINK, 26).move_to([4.55, -2.2, 0])
        self.at("published it")
        route = CurvedArrow(sch.get_bottom() + DOWN * 0.1, clin.get_left() + LEFT * 0.1, angle=TAU / 8, color=GOLD,
                            stroke_width=5)
        self.play(Create(route), run_time=0.7)
        self.at("clinical journal")
        self.play(pop(clin), run_time=0.5)
        self.play(Indicate(clin, color=PINK, scale_factor=1.08), run_time=0.8)
        self.at("biochemical one")
        blocked = arrow(sch.get_right() + RIGHT * 0.1, biochem.get_left() + LEFT * 0.1, RED, 4, 0.2)
        blocked.set_stroke(opacity=0.8)
        cross = VGroup(Line(UL * 0.3, DR * 0.3, color=RED, stroke_width=7), Line(UR * 0.3, DL * 0.3, color=RED, stroke_width=7))
        cross.move_to(blocked.get_center())
        self.play(pop(biochem), GrowArrow(blocked), run_time=0.6)
        self.play(Create(cross), run_time=0.5)
        ctrl = Line(grip.get_bottom() + DOWN * 0.05, biochem.get_top() + UP * 0.05, color=RED, stroke_width=4)
        ctl = T("controlled", 24, RED).next_to(ctrl, RIGHT, buff=0.15)
        self.at("controlled")
        self.play(Create(ctrl), FadeIn(ctl), run_time=0.6)

        # the first correct map
        self.at("It was the first", lead=0.4)
        self.play(FadeOut(VGroup(sch, grip, biochem, clin, route, blocked, cross, ctrl, ctl, yr)), run_time=0.4)
        first = T("the first correct map", 40, GOLD, font=TITLE_FONT).move_to([PANEL_C, 2.4, 0])
        ul = Line(first.get_corner(DL) + DOWN * 0.1, first.get_corner(DR) + DOWN * 0.1, color=GOLD, stroke_width=4)
        self.at("first correct map")
        self.play(FadeIn(first, shift=UP * 0.1), Create(ul), run_time=0.7)

        glc2 = lab("glucose", GREEN, 30).move_to([-0.2, 0.7, 0])
        eng = lab("energy", TEXT, 30).move_to([4.4, 0.7, 0])
        a_e = arrow(glc2.get_right() + RIGHT * 0.1, eng.get_left() + LEFT * 0.1, TEXT, 5, 0.25)
        cell = T("a cell pulls", 24, TEXT).next_to(a_e, UP, buff=0.12)
        self.at("how a cell pulls")
        self.play(GrowArrow(a_e), FadeIn(cell), run_time=0.5)
        self.at("energy from glucose")
        self.play(pop(eng), pop(glc2), run_time=0.5)
        ox = lab("oxygen", GREY, 30).move_to([PANEL_C + 0.8, -1.4, 0])
        wo = T("without", 30, RED).next_to(ox, LEFT, buff=0.3)
        self.at("without oxygen")
        self.play(FadeIn(wo), pop(ox), run_time=0.5)
        c = ox.get_center()
        xs = Line(c + [-0.7, 0.38, 0], c + [0.7, -0.38, 0], color=RED, stroke_width=6)
        xs2 = Line(c + [-0.7, -0.38, 0], c + [0.7, 0.38, 0], color=RED, stroke_width=6)
        self.play(Create(xs), Create(xs2), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s04 legacy
class S04Legacy(ProfileScene):
    def construct(self):
        self.add_inset()
        heart = lab("his heart failed", RED, 30).move_to([0.3, 2.6, 0])
        self.at("His heart failed")
        self.play(pop(heart), run_time=0.5)
        yr = M("1933", 52, YELLOW).move_to([4.3, 2.6, 0])
        self.at("1933")
        self.play(Write(yr), run_time=0.5)

        nazi = lab("the Nazis", RED, 30).move_to([PANEL_C, 1.45, 0])
        self.at("the Nazis")
        self.play(pop(nazi), run_time=0.45)
        inst = lab("his institute dismantled", RED, 28).move_to([PANEL_C, 0.0, 0])
        a1 = arrow(nazi.get_bottom() + DOWN * 0.05, inst.get_top() + UP * 0.05, RED, 4, 0.4)
        self.at("dismantled his institute")
        self.play(GrowArrow(a1), pop(inst), run_time=0.6)
        col = lab("his Jewish colleagues dismissed", RED, 28).move_to([PANEL_C, -1.45, 0])
        a2 = arrow(inst.get_bottom() + DOWN * 0.05, col.get_top() + UP * 0.05, RED, 4, 0.4)
        self.at("dismissed his Jewish")
        self.play(GrowArrow(a2), pop(col), run_time=0.6)

        # Europe: the pathway still bears his name first
        self.at("Across much of", lead=0.5)
        self.play(FadeOut(VGroup(heart, yr, nazi, inst, a1, col, a2)), run_time=0.4)
        eu = lab("across much of Europe", PLACE, 30).move_to([PANEL_C, 2.4, 0])
        self.at("Across much of")
        self.play(pop(eu), run_time=0.5)
        pw = T("the pathway still bears", 32, TEXT, font=TITLE_FONT).move_to([PANEL_C, 1.2, 0])
        self.at("the pathway")
        self.play(FadeIn(pw, shift=UP * 0.1), run_time=0.5)
        first = T("his name first", 36, GOLD, font=TITLE_FONT).move_to([PANEL_C, 0.4, 0])
        self.at("his name first")
        self.play(FadeIn(first, shift=UP * 0.1), run_time=0.5)

        # one Text object so all three names share a baseline
        names = T("Embden–Meyerhof–Parnas", 46, GREY, font=TITLE_FONT).move_to([PANEL_C, -1.5, 0])
        fit(names, max_w=8.4)
        n1, d1, n2, d2, n3 = names[0:6], names[6:7], names[7:15], names[15:16], names[16:22]
        n1.set_color(GOLD)
        ul = Line(n1.get_corner(DL) + DOWN * 0.1, n1.get_corner(DR) + DOWN * 0.1, color=GOLD, stroke_width=4)
        self.at("Meyerhof", lead=0.7)
        self.play(FadeIn(n1, shift=UP * 0.1), Create(ul), run_time=0.5)
        self.at("Meyerhof")
        self.play(FadeIn(VGroup(d1, n2), shift=UP * 0.1), run_time=0.4)
        self.at("Parnas")
        self.play(FadeIn(VGroup(d2, n3), shift=UP * 0.1), run_time=0.4)
        self.finish()


# ----------------------------------------------------------------------------- s05 quote
class S05Quote(ProfileScene):
    def construct(self):
        self.add_inset()
        lines = ["“meticulous cleanliness", "and rigorous accuracy”"]
        q = VGroup(*[T(l, 44, TEXT, font=TITLE_FONT) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        fit(q, max_w=8.4)
        who = T("— Gustav Embden", 32, GOLD)
        sub = T("the standard he worked under", 26, GREY)
        g = VGroup(q, who, sub).arrange(DOWN, aligned_edge=RIGHT, buff=0.45).move_to([PANEL_C, 0.1, 0])
        for m in (*q, who, sub):
            m.set_opacity(0)
        self.add(g)
        self.wait(0.4)
        for ln in q:
            self.play(ln.animate.set_opacity(1.0), run_time=0.9)
        self.wait(0.6)
        self.play(who.animate.set_opacity(1.0), sub.animate.set_opacity(1.0), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s06 end card
class S06End(EndCard):
    LINE = "First correct chemical map of glucose to pyruvate, against a twenty-year consensus."

    def construct(self):
        img, frame = portrait_pair(2.3)
        grp = Group(img, frame).move_to([0, 1.95, 0])
        cap = caption_under(frame)
        a = T("First correct chemical map of glucose to pyruvate,", size=40, font=TITLE_FONT)
        b = T("against a twenty-year consensus.", size=40, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.2).move_to([0, -0.7, 0])
        fit(line, max_w=11.8)
        sub = T("biochemistrypedia.com", size=24, color=TEAL).move_to([0, -1.95, 0])
        src = T("Source: The Molecule Hunters (v10) · Embden–Meyerhof–Parnas profile", size=22, color=GREY).move_to([0, -2.7, 0])
        self.play(FadeIn(img), FadeIn(frame), FadeIn(cap), run_time=0.5)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(sub), FadeIn(src), run_time=0.4)
        self.finish()
