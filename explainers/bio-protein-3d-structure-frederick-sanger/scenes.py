"""Frederick Sanger: a scientist profile (Biochemistrypedia, protein-3d-structure lesson).

Narration is the lesson entry's `story`, verbatim. Everything on screen comes from that entry
(name, dates, contribution, story, quotes). The portrait is an AI-generated engraving-style
illustration from The Molecule Hunters (cropped to the figure); it is captioned
"illustration · AI-generated" whenever it is on screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = time and recognition: name/dates, the twelve years, 1977/1980, the Nobel prizes, the knighthood
  TEAL   = Sanger's protein work: insulin, the amino-acid tiles, "the answer"
  SULFUR = disulfide / sulfur bridges (pink)
  YELLOW = tools and reagents: the trace of thioglycolic acid
  RED    = what stood in the way: the lying molecule, the declined honor (the cross)
  GREEN  = DNA: the genome work, and the fixed order that reads out
  WHITE serif = his own words: "academically not brilliant", "it had better be good", the quote scene
  PLACE (lavender) = places and institutions: Cambridge, Tennis Court Road, Hinxton, the garden
  GREY   = axes, time-of-life labels, de-emphasized things
No molecular structure is drawn: insulin is two bars / rows of plain residue tiles, and the sulfur
bridges are plain links between them.
"""
import os
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

IMG = Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent / "sanger_crop.png"
CROP_AR = 860 / 780.0   # sanger_crop.png: the engraving cropped to the figure (from public/scientists/frederick-sanger.png)
CAPTION = "illustration · AI-generated"
PLACE = "#B39DDB"       # places and institutions
SULFUR = "#E07BB5"      # disulfide / sulfur bridges

INSET_C = np.array([-4.6, 1.25, 0.0])
INSET_H = 3.0
PANEL_C = 1.95          # x center of the right panel (x from -2.4 to 6.3)


# ----------------------------------------------------------------------------- helpers
def portrait_pair(height):
    img = ImageMobject(str(IMG)).set_height(height)
    frame = Rectangle(width=img.width, height=img.height, stroke_color=GOLD, stroke_width=3, fill_opacity=0)
    return img, frame


def caption_under(frame, size=22):
    return T(CAPTION, size=size, color=GREY, font=TITLE_FONT).next_to(frame, DOWN, buff=0.2)


def name_tag(frame):
    nm = T("Frederick Sanger", size=32, font=TITLE_FONT)
    fit(nm, max_w=3.5)
    dt = T("1918–2013", size=28, color=GOLD)
    g = VGroup(nm, dt).arrange(DOWN, buff=0.14)
    g.move_to([frame.get_center()[0], frame.get_center()[1] - INSET_H / 2 - 1.25, 0])
    return g


def inset_group():
    img, frame = portrait_pair(INSET_H)
    img.move_to(INSET_C)
    frame.move_to(INSET_C)
    cap = caption_under(frame)
    tag = name_tag(frame)
    rule = Line([-2.7, -3.2, 0], [-2.7, 3.2, 0], color=GREY, stroke_width=1.5).set_opacity(0.35)
    return img, frame, cap, tag, rule


def lab(lines, color=BLUE, size=28, pad=0.22, fill=0.16, font=FONT):
    """Chip with one or more centered lines of text."""
    if isinstance(lines, str):
        lines = [lines]
    txt = VGroup(*[T(l, size, color, font=font) for l in lines]).arrange(DOWN, buff=0.1)
    ref_h = len(lines) * T("Ag", size).height + (len(lines) - 1) * 0.1
    box = RoundedRectangle(corner_radius=0.14, width=txt.width + 2 * pad, height=max(txt.height, ref_h) + 2 * pad,
                           stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=fill)
    return VGroup(box, txt.move_to(box))


def pop(mob):
    return FadeIn(mob, shift=UP * 0.12)


def cross(center, color=RED, r=0.26, w=8):
    return VGroup(Line([-r, -r, 0], [r, r, 0]), Line([-r, r, 0], [r, -r, 0])).set_color(color) \
        .set_stroke(width=w).move_to(center)


class ProfileScene(SpokenScene):
    def add_inset(self):
        img, frame, cap, tag, rule = inset_group()
        self.add(img, frame, cap, tag, rule)


def tilesq(x, y, color=TEAL, s=0.2):
    return Rectangle(width=s, height=s, stroke_color=color, stroke_width=1.5,
                     fill_color=ManimColor(BG).interpolate(ManimColor(color), 0.35), fill_opacity=1).move_to([x, y, 0])


# ----------------------------------------------------------------------------- s00 title
class S00Title(TitleCard):
    LESSON = "Scientist profile"
    TITLE = "Frederick Sanger"

    def construct(self):
        img, frame = portrait_pair(4.2)
        grp = Group(img, frame)
        grp.move_to([-3.8, 0.35, 0])
        cap = caption_under(frame, size=24).shift(DOWN * 0.1)
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        name = T(self.TITLE, size=50, font=TITLE_FONT)
        dates = T("1918–2013", size=38, color=GOLD)
        rule = Line(LEFT * 1.2, RIGHT * 1.2, color=GOLD, stroke_width=4)
        txt = VGroup(brand, lesson, name, dates, rule).arrange(DOWN, buff=0.3).move_to([2.6, 0.2, 0])
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


# ----------------------------------------------------------------------------- s01 twelve years
class S01Years(ProfileScene):
    def construct(self):
        self.add_inset()
        # twelve one-year blocks, filling as "twelve years" is spoken
        bx0, pitch, bw, by = 0.1, 0.5, 0.4, 2.6
        blocks = VGroup(*[Rectangle(width=bw, height=0.5, stroke_color=GOLD, stroke_width=2, fill_color=GOLD,
                                    fill_opacity=0.55).move_to([bx0 + pitch * i + bw / 2, by, 0]) for i in range(12)])
        yrs = T("12 years", 36, GOLD, weight=BOLD).move_to([-1.2, by, 0])
        self.at("twelve years")
        self.play(FadeIn(yrs, shift=RIGHT * 0.1), LaggedStart(*[FadeIn(b, scale=1.4) for b in blocks], lag_ratio=0.12),
                  run_time=1.3)

        mol = lab("one molecule", TEAL, 36).move_to([PANEL_C, 1.2, 0])
        self.at("single molecule")
        self.play(pop(mol), run_time=0.5)

        # the place: the molecule chip turns into the street, then the city wraps around it
        street = lab("Tennis Court Road", PLACE, 32).move_to([0.0, 1.2, 0])
        region = RoundedRectangle(corner_radius=0.2, width=8.5, height=1.5, stroke_color=PLACE, stroke_width=2.5,
                                  fill_color=PLACE, fill_opacity=0.08).move_to([PANEL_C, 1.2, 0])
        city = T("Cambridge", 38, PLACE).move_to([4.5, 1.2, 0])
        self.at("Tennis Court Road")
        self.play(ReplacementTransform(mol, street), run_time=0.7)
        self.at("Cambridge")
        self.play(FadeIn(region), pop(city), run_time=0.6)

        quaker = lab("Quaker conscientious objector", TEXT, 30).move_to([PANEL_C - 0.2, -0.1, 0])
        quaker.align_to(np.array([-2.3, 0, 0]), LEFT)
        self.at("Quaker conscientious objector")
        self.play(pop(quaker), run_time=0.6)
        war = T("the war", 26, GREY).move_to([-2.3, -0.9, 0], aligned_edge=LEFT)
        scrub = lab("scrubbing hospital toilets with a mop", TEXT, 30).move_to([PANEL_C, -1.7, 0])
        scrub.align_to(np.array([-2.3, 0, 0]), LEFT)
        self.at("the war")
        self.play(FadeIn(war, shift=UP * 0.05), run_time=0.3)
        self.at("scrubbing hospital toilets")
        self.play(pop(scrub), run_time=0.6)

        quote = lab("“academically not brilliant”", TEXT, 32, font=TITLE_FONT).move_to([PANEL_C, -2.8, 0])
        quote.align_to(np.array([-2.3, 0, 0]), LEFT)
        self.at("academically not brilliant")
        self.play(pop(quote), run_time=0.7)

        # last beat: three years over the first part of the degree
        self.at("He had taken three years")
        old = VGroup(blocks, yrs, street, region, city, quaker, war, scrub)
        self.play(FadeOut(old), quote.animate.move_to([PANEL_C, 2.1, 0]), run_time=0.6)
        years3 = VGroup(*[Rectangle(width=1.0, height=0.8, stroke_color=GOLD, stroke_width=2.5, fill_color=GOLD,
                                    fill_opacity=0.55).move_to([-0.3 + 1.2 * i, 0.4, 0]) for i in range(3)])
        y3 = T("3 years", 36, GOLD, weight=BOLD).move_to([4.25, 0.4, 0])
        self.at("three years")
        self.play(LaggedStart(*[FadeIn(b, scale=1.3) for b in years3], lag_ratio=0.25), FadeIn(y3, shift=LEFT * 0.1),
                  run_time=0.9)
        degree = lab("first part of his degree", TEXT, 30).move_to([1.2, -1.2, 0])
        self.at("first part of his degree")
        self.play(pop(degree), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s02 insulin fought him
class S02Insulin(ProfileScene):
    X0 = -1.6
    TOP_Y, BOT_Y = 1.1, -0.9
    # link layouts: (arc xa, xb) on the top bar, then two top->bottom links (x_top, x_bottom)
    STATES = {
        "true": ((-0.38, 0.58), (-0.21, -0.22), (2.39, 2.18)),
        "s1": ((0.4, 1.6), (-1.1, 1.0), (1.4, 3.6)),
        "s2": ((-1.2, 0.2), (0.2, 3.0), (2.2, -0.4)),
        "s3": ((1.0, 2.2), (-0.9, 1.9), (1.0, 4.0)),
    }

    def bar(self, length, y, color=TEAL):
        return RoundedRectangle(corner_radius=0.1, width=length, height=0.34, stroke_color=color, stroke_width=2.5,
                                fill_color=color, fill_opacity=0.3).move_to([self.X0 + length / 2, y, 0])

    def arc(self, xa, xb):
        return ArcBetweenPoints([xa, self.TOP_Y + 0.17, 0], [xb, self.TOP_Y + 0.17, 0], angle=-PI * 0.8,
                                color=SULFUR, stroke_width=7)

    def vlink(self, xt, xb):
        return Line([xt, self.TOP_Y - 0.17, 0], [xb, self.BOT_Y + 0.17, 0], color=SULFUR, stroke_width=7)

    def to_state(self, links, name):
        arc, v1, v2 = links
        (a, b), (t1, b1), (t2, b2) = self.STATES[name]
        return [
            Transform(arc, self.arc(a, b)),
            v1.animate.put_start_and_end_on([t1, self.TOP_Y - 0.17, 0], [b1, self.BOT_Y + 0.17, 0]),
            v2.animate.put_start_and_end_on([t2, self.TOP_Y - 0.17, 0], [b2, self.BOT_Y + 0.17, 0]),
        ]

    def construct(self):
        self.add_inset()
        ins = lab("insulin", TEAL, 32).move_to([-0.9, 2.95, 0])
        self.at("Insulin")
        self.play(pop(ins), run_time=0.5)
        self.at("fought him")
        self.play(Indicate(ins, color=RED, scale_factor=1.12), run_time=0.7)

        top, bot = self.bar(4.2, self.TOP_Y), self.bar(6.0, self.BOT_Y)
        (a, b), (t1, b1), (t2, b2) = self.STATES["true"]
        links = [self.arc(a, b), self.vlink(t1, b1), self.vlink(t2, b2)]
        dlab = T("disulfide bonds", 30, SULFUR).move_to([4.6, 1.1, 0])
        self.at("disulfide bonds")
        self.play(FadeIn(top), FadeIn(bot), run_time=0.4)
        self.play(LaggedStart(*[Create(l) for l in links], lag_ratio=0.3), FadeIn(dlab, shift=LEFT * 0.1), run_time=0.8)

        # the bonds rearrange themselves, mid-experiment
        mid = lab("mid-experiment", GREY, 28).move_to([-0.7, -2.2, 0])
        self.at("rearranged themselves")
        self.play(*self.to_state(links, "s1"), run_time=0.55)
        self.play(*self.to_state(links, "s2"), pop(mid), run_time=0.55)
        self.play(*self.to_state(links, "s3"), run_time=0.55)
        self.play(*self.to_state(links, "s1"), run_time=0.55)

        # the molecule effectively lying about its own structure
        lie = lab(["lying to him", "about its own structure"], RED, 28).move_to([3.45, -2.15, 0])
        lie[1][1].set_opacity(0)
        self.at("effectively lying")
        self.play(FadeIn(lie[0]), FadeIn(lie[1][0]), *self.to_state(links, "s2"), run_time=0.6)
        self.play(*self.to_state(links, "s3"), run_time=0.6)
        self.play(*self.to_state(links, "s1"), run_time=0.6)
        self.at("its own structure")
        self.play(lie[1][1].animate.set_opacity(1), *self.to_state(links, "s2"), run_time=0.6)

        # caught with a trace of thioglycolic acid: one drop, the bonds snap to the true layout and pin
        drop = Dot([3.9, 3.0, 0], radius=0.1, color=YELLOW)
        self.at("until he caught", lead=0.3)
        self.add(drop)
        self.play(FadeOut(lie), FadeOut(mid), drop.animate.move_to([2.3, 0.1, 0]), run_time=0.5, rate_func=rush_into)
        self.play(Flash(drop.get_center(), color=YELLOW, flash_radius=0.4), FadeOut(drop),
                  *self.to_state(links, "true"), run_time=0.6)
        pins = VGroup(*[Dot(p, radius=0.09, color=TEAL).set_z_index(3) for p in [
            [-0.38, self.TOP_Y + 0.17, 0], [0.58, self.TOP_Y + 0.17, 0],
            [-0.21, self.TOP_Y - 0.17, 0], [-0.22, self.BOT_Y + 0.17, 0],
            [2.39, self.TOP_Y - 0.17, 0], [2.18, self.BOT_Y + 0.17, 0]]])
        self.play(FadeIn(pins, scale=2), run_time=0.3)
        acid = lab("thioglycolic acid", YELLOW, 28).move_to([4.2, 2.95, 0])
        self.at("thioglycolic acid")
        self.play(pop(acid), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s03 the answer
class S03Answer(ProfileScene):
    def construct(self):
        self.add_inset()
        px0, pitch = -2.1, 0.255
        top_y, bot_y = 0.7, -1.1

        yr = T("1955", 44, GOLD, weight=BOLD).move_to([-1.35, 2.95, 0])
        self.at("1955")
        self.play(pop(yr), run_time=0.5)
        ans = lab("the published answer", TEAL, 30).move_to([2.9, 2.95, 0])
        self.at("published the answer")
        self.play(pop(ans), run_time=0.5)

        # 51 residue tiles fill two rows, with a counter
        bot_tiles = [tilesq(px0 + pitch * i, bot_y + 0.35) for i in range(30)]   # start close, separate on "two chains"
        top_tiles = [tilesq(px0 + pitch * i, top_y - 0.35) for i in range(21)]
        allt = top_tiles + bot_tiles
        n = ValueTracker(0)
        counter = always_redraw(lambda: M(f"{int(round(n.get_value()))}", 52, TEAL, weight=BOLD)
                                .move_to([-1.55, 2.0, 0]))
        aa = T("amino acids", 34, TEAL).move_to([0.6, 2.0, 0])
        aa.align_to(np.array([-0.6, 0, 0]), LEFT)
        self.at("51 amino acids")
        self.add(counter)
        self.play(FadeIn(aa, shift=LEFT * 0.1),
                  n.animate.set_value(51),
                  LaggedStart(*[FadeIn(t, scale=1.5) for t in allt], lag_ratio=0.03),
                  run_time=1.4, rate_func=linear)
        counter.clear_updaters()

        # two chains: the rows pull apart
        c1 = T("chain", 28, TEAL).move_to([px0 + 0.3, top_y + 0.55, 0])
        c2 = T("chain", 28, TEAL).move_to([px0 + 0.3, bot_y - 0.55, 0])
        self.at("two chains")
        self.play(*[t.animate.shift(UP * 0.35) for t in top_tiles], *[t.animate.shift(DOWN * 0.35) for t in bot_tiles],
                  FadeIn(c1), FadeIn(c2), run_time=0.7)

        # three sulfur bridges: two links between the rows and one within the upper row
        xi = lambda i: px0 + pitch * i
        arc = ArcBetweenPoints([xi(5), top_y + 0.12, 0], [xi(10), top_y + 0.12, 0], angle=-PI * 0.8,
                               color=SULFUR, stroke_width=6)
        v1 = Line([xi(6), top_y - 0.12, 0], [xi(6), bot_y + 0.12, 0], color=SULFUR, stroke_width=6)
        v2 = Line([xi(19), top_y - 0.12, 0], [xi(18), bot_y + 0.12, 0], color=SULFUR, stroke_width=6)
        sb = lab(["3 sulfur", "bridges"], SULFUR, 28).move_to([4.7, -0.2, 0])
        self.at("three sulfur bridges")
        self.play(LaggedStart(Create(arc), Create(v1), Create(v2), lag_ratio=0.35), pop(sb), run_time=1.0)

        # in one fixed order: a reading wave runs along each chain
        fixed = lab("one fixed order", GREEN, 34).move_to([1.2, -2.75, 0])
        self.at("one fixed order")
        self.play(pop(fixed),
                  LaggedStart(*[t.animate.set_stroke(GREEN, 2.5).set_fill(GREEN, 0.55) for t in top_tiles], lag_ratio=0.04),
                  run_time=0.9)
        self.play(LaggedStart(*[t.animate.set_stroke(GREEN, 2.5).set_fill(GREEN, 0.55) for t in bot_tiles], lag_ratio=0.03),
                  run_time=0.8)
        self.finish()


# ----------------------------------------------------------------------------- s04 again with DNA
class S04Again(ProfileScene):
    def construct(self):
        self.add_inset()
        ay = 2.5
        xy = lambda yr: -1.8 + (yr - 1955) * 0.27
        axis = Arrow([-2.2, ay, 0], [6.1, ay, 0], color=GREY, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.04)
        d55, d77, d80 = (Dot([xy(y), ay, 0], radius=0.12, color=GOLD) for y in (1955, 1977, 1980))
        l55 = T("1955", 30, GOLD, weight=BOLD).move_to([xy(1955), ay + 0.5, 0])
        l77 = T("1977", 30, GOLD, weight=BOLD).move_to([xy(1977) - 0.25, ay + 0.5, 0])
        l80 = T("1980", 30, GOLD, weight=BOLD).move_to([xy(1980) + 0.15, ay - 0.5, 0])
        ins = lab("insulin", TEAL, 30).move_to([-1.0, 0.95, 0])
        self.add(axis, d55, l55)
        self.at("He did it again")
        self.play(pop(ins), run_time=0.5)

        dna = lab("DNA", GREEN, 30).move_to([xy(1977), 0.95, 0])
        arrow = Arrow(ins.get_right() + RIGHT * 0.1, dna.get_left() + LEFT * 0.1, color=TEXT, stroke_width=4, buff=0,
                      max_tip_length_to_length_ratio=0.15)
        again = T("again", 28, TEXT).next_to(arrow, UP, buff=0.12)
        self.at("with DNA")
        self.play(GrowArrow(arrow), FadeIn(again), pop(dna), run_time=0.7)
        self.at("1977")
        self.play(FadeIn(d77, scale=2), FadeIn(l77, shift=UP * 0.1), run_time=0.5)

        genome = lab(["first complete", "DNA genome"], GREEN, 28).move_to([xy(1977) - 0.55, -0.7, 0])
        link = Line(dna.get_bottom(), [xy(1977), genome.get_top()[1], 0], color=GREEN, stroke_width=3)
        self.at("sequenced the first complete DNA genome")
        self.play(Create(link), pop(genome), run_time=0.7)

        # second Nobel, 1980
        stageA = VGroup(axis, d55, l55, d77, l77, ins, dna, arrow, again, genome, link)
        self.at("and took", lead=0.4)
        self.play(FadeOut(stageA), run_time=0.4)

        dim = interpolate_color(ManimColor(GOLD), ManimColor(BG), 0.55)

        def medal(x, color=GOLD):
            ring = Circle(radius=0.8, stroke_color=color, stroke_width=5, fill_color=color, fill_opacity=0.18)
            inner = Circle(radius=0.62, stroke_color=color, stroke_width=2, fill_opacity=0)
            mark = T("N", 44, color, font=TITLE_FONT, weight=BOLD)
            return VGroup(ring, inner, mark).move_to([x, 1.1, 0])

        m1, m2 = medal(0.3, dim), medal(4.1)
        t1 = T("first Nobel", 28, GREY).next_to(m1, DOWN, buff=0.3)
        t2 = T("second Nobel", 30, GOLD).next_to(m2, DOWN, buff=0.3)
        y80 = T("1980", 40, GOLD, weight=BOLD).next_to(m2, UP, buff=0.3)
        self.at("took a second Nobel")
        self.play(FadeIn(m1, scale=0.8), FadeIn(t1), run_time=0.3)
        self.at("second Nobel")
        self.play(FadeIn(m2, scale=0.6), FadeIn(t2), run_time=0.6)
        self.at("1980")
        self.play(pop(y80), run_time=0.4)

        only1 = T("the only person of the century", 34, TEXT, font=TITLE_FONT).move_to([PANEL_C, -1.5, 0])
        only2 = T("to win the chemistry prize twice", 34, GOLD, font=TITLE_FONT).move_to([PANEL_C, -2.25, 0])
        self.at("the only person of the century")
        self.play(pop(only1), run_time=0.7)
        self.at("win the chemistry prize")
        self.play(pop(only2), run_time=0.7)
        self.at("twice")
        self.play(m1.animate.set_color(GOLD), Indicate(m2, color=GOLD, scale_factor=1.12), run_time=0.8)

        # declined a knighthood, did not want to be different
        stageB = Group(m1, m2, t1, t2, y80, only1, only2)
        self.at("He declined a knighthood", lead=0.35)
        self.play(FadeOut(stageB), run_time=0.4)
        circles = VGroup(*[Circle(radius=0.38, stroke_color=TEXT, stroke_width=3, fill_color=TEXT, fill_opacity=0.12)
                           .move_to([-0.9 + 1.4 * i, -0.3, 0]) for i in range(5)])
        self.play(LaggedStart(*[FadeIn(c, scale=0.7) for c in circles], lag_ratio=0.1), run_time=0.5)
        knight = lab("knighthood", GOLD, 36).move_to([PANEL_C - 0.4, 1.9, 0])
        karrow = Arrow(knight.get_bottom() + DOWN * 0.05, circles[2].get_top() + UP * 0.1, color=GOLD, stroke_width=4,
                       buff=0, max_tip_length_to_length_ratio=0.3)
        self.at("knighthood")
        self.play(pop(knight), GrowArrow(karrow), run_time=0.5)
        self.play(circles[2].animate.set_stroke(GOLD).set_fill(GOLD, 0.55), run_time=0.4)
        no = cross(karrow.get_center() + RIGHT * 0.0, r=0.3, w=9)
        self.at("did not want")
        self.play(FadeIn(no, scale=1.4), knight.animate.set_opacity(0.45), karrow.animate.set_opacity(0.45),
                  circles[2].animate.set_stroke(TEXT).set_fill(TEXT, 0.12), run_time=0.5)
        diff = T("different", 32, GOLD, weight=BOLD).next_to(circles[2], DOWN, buff=0.35)
        strike = Line(diff.get_left() + LEFT * 0.08, diff.get_right() + RIGHT * 0.08, color=RED, stroke_width=5)
        self.at("different")
        self.play(pop(diff), run_time=0.35)
        self.play(Create(strike), run_time=0.3)

        # retired at 65 to the garden
        ret = lab(["retired", "at 65"], GOLD, 36).move_to([-0.1, 0.4, 0])
        garden = lab("his garden", PLACE, 36).move_to([4.2, 0.4, 0])
        ga = Arrow(ret.get_right() + RIGHT * 0.1, garden.get_left() + LEFT * 0.1, color=GREY, stroke_width=4, buff=0,
                   max_tip_length_to_length_ratio=0.3)
        self.at("and retired", lead=0.25)
        self.play(FadeOut(VGroup(circles, knight, karrow, no, diff, strike)), pop(ret), run_time=0.45)
        self.at("to his garden")
        self.play(GrowArrow(ga), pop(garden), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- s05 it had better be good
class S05Creed(ProfileScene):
    def construct(self):
        self.add_inset()
        center = lab(["great genome", "center"], GREEN, 34).move_to([0.3, 2.2, 0])
        self.at("Great Genome Center")
        self.play(pop(center), run_time=0.6)
        hinx = lab("Hinxton", PLACE, 38).move_to([4.3, 2.2, 0])
        self.at("Hingston")
        self.play(pop(hinx), run_time=0.5)

        name = lab("his name", GOLD, 34).move_to([0.3, 0.2, 0])
        arrow = Arrow(name.get_top() + UP * 0.05, center.get_bottom() + DOWN * 0.05, color=GOLD, stroke_width=4, buff=0,
                      max_tip_length_to_length_ratio=0.3)
        self.at("asked to take his name")
        self.play(pop(name), run_time=0.4)
        self.play(GrowArrow(arrow), run_time=0.5)

        cond = lab("his only condition", TEXT, 34).move_to([3.9, 0.2, 0])
        self.at("his only condition")
        self.play(pop(cond), run_time=0.5)

        creed_lab = T("his whole creed", 32, GREY).move_to([PANEL_C, -1.0, 0])
        line = Line([-2.2, -2.6, 0], [6.2, -2.6, 0], color=GREY, stroke_width=2).set_opacity(0.5)
        self.at("a sentence that could stand")
        self.play(Create(line), run_time=0.6)
        self.at("whole creed")
        self.play(FadeIn(creed_lab, shift=UP * 0.1), run_time=0.5)

        words = ["it", "had", "better", "be", "good."]
        ws = VGroup(*[T(w, 56, TEXT, font=TITLE_FONT) for w in words]).arrange(RIGHT, buff=0.3)
        ws.move_to([PANEL_C, -1.9, 0])
        for i, w in enumerate(words):
            self.at(w.strip("."), lead=0.1)
            self.play(FadeIn(ws[i], shift=UP * 0.12), run_time=0.25)
        self.finish()


# ----------------------------------------------------------------------------- s06 the quote
class S06Quote(ProfileScene):
    def construct(self):
        self.add_inset()
        lines = ["“Practically nothing was known about", "the relative order in which these", "residues were arranged in the", "molecules.”"]
        para = Paragraph(*lines, font=TITLE_FONT, font_size=38, color=TEXT, alignment="left", line_spacing=1.0)
        q = VGroup(*para.chars)   # one row per line, laid out on even baselines
        fit(q, max_w=8.4)
        who = T("— Frederick Sanger", 32, GOLD)
        g = VGroup(q, who).arrange(DOWN, aligned_edge=RIGHT, buff=0.55).move_to([PANEL_C, 0.1, 0])
        for ln in q:
            ln.set_opacity(0)
        who.set_opacity(0)
        self.add(g)
        self.wait(0.3)
        for ln in q:
            self.play(ln.animate.set_opacity(1.0), run_time=0.7)
        self.wait(0.4)
        self.play(who.animate.set_opacity(1.0), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s07 end card
class S07End(EndCard):
    LINE = "Read insulin, the first protein sequence, in 1955; invented DNA sequencing."

    def construct(self):
        a = T("Read insulin, the first protein sequence, in 1955;", size=40, font=TITLE_FONT)
        b = T("invented DNA sequencing.", size=40, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.22)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
