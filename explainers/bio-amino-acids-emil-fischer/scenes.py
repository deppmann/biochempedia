"""Emil Fischer: a scientist profile (Biochemistrypedia, amino-acids lesson).

Narration is the lesson entry's `story`, verbatim. Everything on screen comes from that entry
(name, dates, contribution, story, quotes). The portrait is an AI-generated engraving-style
illustration from The Molecule Hunters (cropped to the figure); it is captioned
"illustration · AI-generated" whenever it is on screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = time: Fischer's name/dates, timeline markers and date labels
  TEAL   = Fischer's chemistry: the instinct, "peptides", the peptide bond, the 1894 declaration
  YELLOW = substances and data: sugars, proteins, amino acids, phenylhydrazine, behavior
  RED    = what went wrong or stood in the way: written off, the poison, the cancer, the losses, vitalism
  PLACE (lavender) = places and institutions: Germany, the congress, Karlsbad
  PEER (orange) = other scientists: Hofmeister, Buchner
  GREY   = axes, rulers, de-emphasized things
No molecular structure is drawn: amino acids are labelled chips, the bond is a plain link between them.
"""
import os
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

PORTRAIT = str(Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent / "fischer_crop.png")
CROP_AR = 475 / 412.0   # fischer_crop.png: figure cropped from public/scientists/emil-fischer.png
CAPTION = "illustration · AI-generated"
NAME = "Emil Fischer"
DATES = "1852–1919"
PLACE = "#B39DDB"       # places and institutions
PEER = "#F2A65A"        # other scientists

INSET_C = np.array([-4.55, 1.2, 0.0])
INSET_H = 2.9
PANEL_C = 1.95          # x center of the right panel (x from -2.4 to 6.3)


# ----------------------------------------------------------------------------- helpers
def portrait_pair(height):
    img = ImageMobject(PORTRAIT).set_height(height)
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


def arrow(a, b, color=GREY, sw=4, buff=0.08):
    return Arrow(a, b, color=color, stroke_width=sw, buff=buff, max_tip_length_to_length_ratio=0.35)


def xmark(center, color=RED, r=0.24, sw=8):
    return VGroup(Line([-r, -r, 0], [r, r, 0]), Line([-r, r, 0], [r, -r, 0])).set_color(color).set_stroke(width=sw) \
        .move_to(center)


class ProfileScene(SpokenScene):
    def add_inset(self):
        img, frame, cap, tag, rule = inset_group()
        self.add(img, frame, cap, tag, rule)


# ----------------------------------------------------------------------------- s00 title
class S00Title(TitleCard):
    LESSON = "Scientist profile"
    TITLE = NAME

    def construct(self):
        img, frame = portrait_pair(4.1)
        grp = Group(img, frame)
        grp.move_to([-3.3, 0.45, 0])
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


# ----------------------------------------------------------------------------- s01 merchant's son to chemist
class S01Merchant(ProfileScene):
    def construct(self):
        self.add_inset()
        cx = PANEL_C
        son = lab("lumber merchant's son", TEXT, 30).move_to([cx, 2.75, 0])
        self.at("lumber")
        self.play(pop(son), run_time=0.45)

        quote = lab("“too stupid to be a businessman”", RED, 28).move_to([cx, 1.5, 0])
        self.at("written off")
        self.play(pop(quote), run_time=0.45)
        strike = Line(quote.get_left() + RIGHT * 0.12, quote.get_right() - RIGHT * 0.12, color=RED, stroke_width=5)
        self.at("man", lead=0.0)
        self.play(Create(strike), run_time=0.4)

        organic = lab(["most formidable", "organic chemist"], TEAL, 32).move_to([0.45, -0.15, 0])
        down = arrow([0.45, quote.get_bottom()[1] - 0.02, 0], organic.get_top() + UP * 0.02, GREY, 4, 0.0)
        became = T("became", 24, GREY).next_to(down, RIGHT, buff=0.2)
        self.at("became")
        self.play(GrowArrow(down), FadeIn(became), son.animate.set_opacity(0.45), quote.animate.set_opacity(0.45),
                  strike.animate.set_opacity(0.45), run_time=0.5)
        self.at("most formidable")
        self.play(pop(organic), run_time=0.5)
        germany = lab("in Germany", PLACE, 30).move_to([4.7, -0.15, 0])
        self.at("Germany")
        self.play(pop(germany), run_time=0.45)

        structure = lab("structure", TEAL, 30).move_to([4.0, -2.2, 0])
        behavior = lab("behavior", YELLOW, 30).move_to([-0.3, -2.2, 0])
        read = arrow(behavior.get_right() + RIGHT * 0.05, structure.get_left() + LEFT * 0.05, TEXT, 4, 0.0)
        read_lab = T("read off", 24, GREY).next_to(read, UP, buff=0.12)
        self.at("reading")
        self.play(pop(structure), run_time=0.45)
        self.at("behavior")
        self.play(pop(behavior), GrowArrow(read), FadeIn(read_lab), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s02 peptides at Karlsbad
class S02Peptide(ProfileScene):
    def construct(self):
        self.add_inset()
        cx = PANEL_C
        instinct = lab("same instinct", TEAL, 30).move_to([cx, 2.2, 0])
        self.at("same instinct")
        self.play(pop(instinct), run_time=0.45)

        sugars = lab("sugars", YELLOW, 30).move_to([-0.2, 0.3, 0])
        cage = DashedVMobject(SurroundingRectangle(sugars, buff=0.22, corner_radius=0.2), num_dashes=36)
        cage.set_color(TEAL).set_stroke(width=4)
        geo = T("geometry", 24, TEAL).next_to(cage, DOWN, buff=0.15)
        a1 = arrow(instinct.get_bottom(), cage.get_top() + UP * 0.02, TEAL, 4, 0.05)
        self.at("cage")
        self.play(Create(cage), GrowArrow(a1), run_time=0.6)
        self.at("geometry")
        self.play(FadeIn(geo), run_time=0.4)
        self.at("sugars")
        self.play(pop(sugars), run_time=0.45)

        proteins = lab("proteins", YELLOW, 30).move_to([4.0, 0.3, 0])
        a2 = arrow(instinct.get_bottom(), proteins.get_top() + UP * 0.02, TEAL, 4, 0.05)
        clear = T("seen clearly", 24, TEAL).next_to(proteins, DOWN, buff=0.35)
        self.at("see proteins")
        self.play(GrowArrow(a2), pop(proteins), run_time=0.6)
        self.at("clearly")
        self.play(FadeIn(clear), run_time=0.4)

        self.at("clearly", lead=-0.7)
        self.play(FadeOut(VGroup(instinct, sugars, cage, geo, a1, a2, proteins, clear)), run_time=0.4)

        # 1902: the congress
        ay = 2.4
        axis = Arrow([-2.2, ay, 0], [6.15, ay, 0], color=GREY, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.04)
        dot = Dot([1.7, ay, 0], radius=0.12, color=GOLD)
        date = T("September 1902", 34, GOLD, weight=BOLD).move_to([1.7, ay + 0.5, 0])
        congress = lab("congress", PLACE, 30).move_to([0.2, 1.3, 0])
        karls = lab("Karlsbad", PLACE, 30).move_to([3.1, 1.3, 0])
        inn = T("in", 26, GREY).move_to([1.65, 1.3, 0])
        self.at("Congress")
        self.play(pop(congress), run_time=0.45)
        self.at("Carlsbad")
        self.play(FadeIn(inn), pop(karls), run_time=0.45)
        self.at("September")
        self.play(Create(axis), FadeIn(dot, scale=2), FadeIn(date, shift=UP * 0.1), run_time=0.6)

        # the word and the bond
        new_word = T("new word", 24, GREY).move_to([4.3, 0.5, 0])
        word = T("“peptides”", 46, TEAL, font=TITLE_FONT).move_to([4.3, -0.1, 0])
        self.at("introduced")
        self.play(FadeIn(new_word), run_time=0.4)
        self.at("peptides")
        self.play(Write(word), run_time=0.8)

        names = lab("peptide bond", TEAL, 30).move_to([0.5, -0.65, 0])
        self.at("named the bond")
        self.play(pop(names), run_time=0.45)

        row_y = -2.1
        aa = [lab("amino acid", YELLOW, 28).move_to([x, row_y, 0]) for x in (-1.0, 2.0, 5.0)]
        link1 = Line(aa[0].get_right(), aa[1].get_left(), color=TEAL, stroke_width=9).set_z_index(0)
        link2 = Line(aa[1].get_right(), aa[2].get_left(), color=TEAL, stroke_width=9).set_z_index(0)
        pointer = arrow(names.get_bottom(), [0.5, row_y + 0.1, 0], TEAL, 4, 0.08)
        self.at("one amino acid")
        self.play(pop(aa[0]), run_time=0.4)
        self.at("to the next")
        self.play(Create(link1), pop(aa[1]), GrowArrow(pointer), run_time=0.7)

        brace = Brace(VGroup(aa[0], aa[2]), DOWN, color=TEAL, buff=0.12)
        back = T("backbone of every protein", 28, TEAL).next_to(brace, DOWN, buff=0.1)
        self.at("backbone")
        self.play(Create(link2), pop(aa[2]), FadeOut(pointer), GrowFromCenter(brace), run_time=0.7)
        self.at("every protein")
        self.play(FadeIn(back, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s03 Hofmeister, 1894, vitalism
class S03Vitalism(ProfileScene):
    def construct(self):
        self.add_inset()
        # --- Hofmeister: same conclusion, independently
        hof = lab("Franz Hofmeister", PEER, 28).move_to([-0.5, 2.6, 0])
        self.at("Franz Hofmeister")
        self.play(pop(hof), run_time=0.45)

        concl = lab(["same amide-bond", "conclusion"], TEAL, 30).move_to([2.0, 0.95, 0])
        a_h = arrow(hof.get_bottom() + RIGHT * 0.6, concl.get_top() + LEFT * 0.7, PEER, 4, 0.06)
        self.at("same amide bond")
        self.play(GrowArrow(a_h), pop(concl), run_time=0.6)

        fis = lab("Fischer", TEAL, 28).move_to([5.2, 2.6, 0])
        a_f = arrow(fis.get_bottom() + LEFT * 0.4, concl.get_top() + RIGHT * 0.7, TEAL, 4, 0.06)
        indep = T("independently", 26, GREY).move_to([2.75, 2.6, 0])
        self.at("independently")
        self.play(pop(fis), GrowArrow(a_f), FadeIn(indep), run_time=0.6)

        cong = lab("that very congress", PLACE, 28).move_to([2.0, -0.45, 0])
        tie = Line(concl.get_bottom(), cong.get_top(), color=PLACE, stroke_width=3)
        self.at("that very Congress")
        self.play(Create(tie), pop(cong), run_time=0.5)

        name_c = lab("the name", TEAL, 28).move_to([-0.6, -1.65, 0])
        fis2 = lab("Fischer's", TEAL, 28).move_to([2.9, -1.65, 0])
        a_n = arrow(name_c.get_right(), fis2.get_left(), TEAL, 4, 0.08)
        self.at("The name")
        self.play(pop(name_c), run_time=0.4)
        self.at("Fischer's", lead=0.3)
        self.play(GrowArrow(a_n), pop(fis2), run_time=0.5)

        insight = lab("the insight", PEER, 28, fill=0.0).move_to([-0.6, -2.8, 0])
        insight_box = DashedVMobject(insight[0], num_dashes=26).set_color(PEER)
        air = T("in the air", 30, PEER, slant=ITALIC).move_to([2.9, -2.8, 0])
        a_i = arrow(insight.get_right(), air.get_left() + LEFT * 0.1, PEER, 4, 0.08)
        self.at("the insight")
        self.play(Create(insight_box), FadeIn(insight[1]), run_time=0.5)
        self.at("in the air")
        self.play(GrowArrow(a_i), FadeIn(air, shift=UP * 0.08), run_time=0.6)

        # --- 1894 lecture
        stage1 = VGroup(hof, concl, a_h, fis, a_f, indep, cong, tie, name_c, fis2, a_n, insight_box, insight[1], air, a_i)
        self.at("In an 1894", lead=0.7)
        self.play(FadeOut(stage1), run_time=0.5)

        ay = 2.4
        x1, x2 = 0.1, 4.3
        axis = Arrow([-2.2, ay, 0], [6.15, ay, 0], color=GREY, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.04)
        d1 = Dot([x1, ay, 0], radius=0.12, color=GOLD)
        l1 = T("1894", 36, GOLD, weight=BOLD).move_to([x1, ay + 0.52, 0])
        self.at("1894")
        self.play(Create(axis), FadeIn(d1, scale=2), FadeIn(l1, shift=UP * 0.1), run_time=0.6)

        lecture = lab("lecture", TEXT, 28).move_to([x1, 1.3, 0])
        self.at("lecture")
        self.play(pop(lecture), run_time=0.45)

        decl = lab(["chemists could now build", "life's active molecules"], TEAL, 28).move_to([x1, -0.05, 0])
        a1 = arrow(lecture.get_bottom(), decl.get_top(), GREY, 4, 0.05)
        self.at("chemists could now build")
        self.play(GrowArrow(a1), pop(decl), run_time=0.6)

        no_org = lab(["“without any assistance", "from a living organism”"], TEAL, 28).move_to([x1, -1.75, 0])
        a2 = arrow(decl.get_bottom(), no_org.get_top(), GREY, 4, 0.05)
        self.at("without any assistance")
        self.play(GrowArrow(a2), pop(no_org), run_time=0.6)

        d2 = Dot([x2, ay, 0], radius=0.12, color=GOLD)
        seg = Line([x1, ay, 0], [x2, ay, 0], color=GOLD, stroke_width=7)
        yrs = T("three years", 30, GOLD, weight=BOLD).move_to([(x1 + x2) / 2 + 0.4, ay + 0.52, 0])
        self.at("Three years")
        self.play(Create(seg), FadeIn(d2, scale=2), FadeIn(yrs, shift=UP * 0.1), run_time=0.7)

        buch = lab(["Buchner's", "cell-free extract"], PEER, 28).move_to([x2 + 0.25, 1.15, 0])
        self.at("Buckner's")
        self.play(pop(buch), run_time=0.5)
        vit = lab("vitalism", RED, 32).move_to([x2 + 0.25, -0.65, 0])
        blow = arrow(buch.get_bottom(), vit.get_top(), RED, 5, 0.06)
        self.at("delivered")
        self.play(GrowArrow(blow), run_time=0.4)
        self.at("vitalism")
        self.play(pop(vit), run_time=0.45)
        cross = Line(vit.get_left() + RIGHT * 0.12, vit.get_right() - RIGHT * 0.12, color=TEXT, stroke_width=5).set_z_index(5)
        blow_lab = T("decisive blow", 28, RED, weight=BOLD).next_to(vit, DOWN, buff=0.4)
        self.at("decisive")
        self.play(FadeIn(blow_lab, shift=UP * 0.1), run_time=0.4)
        self.at("blow")
        self.play(Create(cross), run_time=0.4)
        self.finish()


# ----------------------------------------------------------------------------- s04 the poison
class S04Poison(ProfileScene):
    def construct(self):
        self.add_inset()
        ay = 2.4
        x75, x19 = -1.4, 5.4

        tool = lab("the tool", TEAL, 30).move_to([-0.7, 0.9, 0])
        self.at("tool")
        self.play(pop(tool), run_time=0.45)
        made = lab(["made all of it", "possible"], TEAL, 28).move_to([3.7, 0.9, 0])
        outs = arrow(tool.get_right(), made.get_left(), TEAL, 4, 0.1)
        self.at("made all of it")
        self.play(GrowArrow(outs), pop(made), run_time=0.8)
        killing = lab("also killing him", RED, 28).move_to([3.7, -0.5, 0])
        self.at("killing him")
        self.play(tool.animate.set_color(RED), pop(killing), run_time=0.5)
        self.wait(0.3)
        self.play(FadeOut(VGroup(made, outs, killing)), run_time=0.35)

        phen = lab("phenylhydrazine", YELLOW, 30).move_to([-0.7, 0.9, 0])
        self.at("Phenylhydrazine")
        self.play(ReplacementTransform(tool, phen), run_time=0.7)

        axis = Arrow([-2.2, ay, 0], [6.15, ay, 0], color=GREY, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.04)
        d1 = Dot([x75, ay, 0], radius=0.12, color=GOLD)
        l1 = T("1875", 36, GOLD, weight=BOLD).move_to([x75, ay + 0.52, 0])
        self.at("1875")
        self.play(Create(axis), FadeIn(d1, scale=2), FadeIn(l1, shift=UP * 0.1), run_time=0.6)

        finger = lab("fingerprint sugars", YELLOW, 28).move_to([4.1, 0.9, 0])
        fa = arrow(phen.get_right(), finger.get_left(), YELLOW, 4, 0.08)
        self.at("fingerprint sugars")
        self.play(GrowArrow(fa), pop(finger), run_time=0.6)

        bar = Rectangle(width=x19 - x75, height=0.32, stroke_width=0, fill_color=RED, fill_opacity=0.85)
        bar.move_to([(x19 + x75) / 2, -0.35, 0])
        self.at("poisoned")
        self.play(GrowFromEdge(bar, LEFT), run_time=1.4, rate_func=linear)
        decades = T("decades of bench work", 26, RED).move_to([2.0, -0.92, 0])
        self.at("decades")
        self.play(FadeIn(decades, shift=UP * 0.08), run_time=0.5)

        d2 = Dot([x19, ay, 0], radius=0.12, color=GOLD)
        l2 = T("1919", 36, GOLD, weight=BOLD).move_to([x19, ay + 0.52, 0])
        self.at("1919")
        self.play(FadeIn(d2, scale=2), FadeIn(l2, shift=UP * 0.1), run_time=0.5)

        cancer = lab("inoperable cancer", RED, 28).move_to([-0.5, -2.4, 0])
        self.at("inoperable cancer")
        self.play(pop(cancer), run_time=0.5)
        link = arrow([-0.5, -0.58, 0], cancer.get_top() + UP * 0.02, RED, 4, 0.0)
        cert = T("almost certainly", 24, GREY).move_to([0.95, -1.5, 0])
        self.at("almost certainly")
        self.play(GrowArrow(link), FadeIn(cert), run_time=0.5)

        sons = VGroup(*[Circle(radius=0.3, stroke_color=TEXT, stroke_width=4, fill_color=TEXT, fill_opacity=0.12)
                        .move_to([x, -2.35, 0]) for x in (3.4, 4.3, 5.2)])
        sons_lab = T("his three sons", 24, GREY).move_to([4.3, -3.05, 0])
        self.at("two of his three sons")
        self.play(LaggedStart(*[FadeIn(s, scale=0.6) for s in sons], lag_ratio=0.25), FadeIn(sons_lab), run_time=0.8)
        lost_lab = T("two lost in a single winter of the war", 24, GREY).move_to([3.5, -3.05, 0])
        self.at("lost")
        self.play(*[s.animate.set_color(GREY).set_fill(GREY, opacity=0.05) for s in sons[:2]],
                  ReplacementTransform(sons_lab, lost_lab), run_time=0.8)
        self.at("winter")
        self.play(Indicate(lost_lab, color=TEXT, scale_factor=1.05), run_time=0.7)

        jul = T("July 15", 34, GOLD, weight=BOLD).move_to([x19 - 0.3, ay - 0.6, 0])
        self.at("July 15")
        self.play(FadeIn(jul, shift=UP * 0.1), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s05 the quote
class S05Quote(ProfileScene):
    def construct(self):
        self.add_inset()
        lines = ["“Enzyme and glucoside", "must fit together like", "a lock and key.”"]
        q = VGroup(*[T(l, 42, TEXT, font=TITLE_FONT) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        fit(q, max_w=8.4)
        who = T("— Emil Fischer", 32, GOLD)
        g = VGroup(q, who).arrange(DOWN, aligned_edge=RIGHT, buff=0.55).move_to([PANEL_C, 0.1, 0])
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


# ----------------------------------------------------------------------------- s06 end card
class S06End(EndCard):
    LINE = "Named the peptide bond, built the first synthetic amino acid chains."

    def construct(self):
        a = T("Named the peptide bond,", size=44, font=TITLE_FONT)
        b = T("built the first synthetic amino acid chains.", size=44, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.22)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
