"""Linus Pauling: a scientist profile (Biochemistrypedia, protein-binding-allostery lesson).

Narration is the lesson entry's `story`, verbatim (four sentence-boundary scenes). Everything on screen
comes from that entry (name, dates, contribution, story, quotes). The portrait is an AI-generated
engraving-style illustration from The Molecule Hunters; it is captioned "illustration · AI-generated"
whenever it is on screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = time: name/dates, timeline markers, "first time"
  TEAL   = Pauling and his ideas: his chip, "a molecular disease", the alpha-helix remark
  GREEN  = healthy / normal hemoglobin and its residue (glutamate)
  RED    = sickle-cell hemoglobin and the defect: valine, the differing letter, the crescent, extra charge
  CHAIN (royal blue) = a protein chain (the beta chain strip), "a specific molecule" and "structure"
  YELLOW = tools and data: the electrophoresis cell, "behavior", mutation-targeted drugs
  PLACE (lavender) = places: Oxford
  GREY   = axes, ghosts of starting positions, the night moon, de-emphasized things
No molecular structure is drawn: hemoglobins are labelled chips, sequences are strips of plain tiles,
and the red cell is a flat disc that turns into a crescent.
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PORTRAIT = str(Path(__file__).resolve().parent / "lp_crop.png")   # crop of public/scientists/linus-pauling.png
CAPTION = "illustration · AI-generated"
PLACE = "#B39DDB"       # places and institutions
CHAIN = "#6F93F2"       # a protein chain / "structure" (BLUE #58C4DD reads too close to TEAL)

INSET_C = np.array([-4.6, 1.15, 0.0])
INSET_H = 3.2
PANEL_C = 1.95          # x center of the right panel (x from -2.4 to 6.3)


# ----------------------------------------------------------------------------- helpers
def portrait_pair(height):
    img = ImageMobject(PORTRAIT).set_height(height)
    frame = Rectangle(width=img.width, height=img.height, stroke_color=GOLD, stroke_width=3, fill_opacity=0)
    return img, frame


def caption_under(frame, size=22):
    return T(CAPTION, size=size, color=GREY, font=TITLE_FONT).next_to(frame, DOWN, buff=0.2)


def name_tag(frame):
    nm = T("Linus Pauling", size=34, font=TITLE_FONT)
    dt = T("1901–1994", size=28, color=GOLD)
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


def tile(label, color=BLUE, size=0.6, fs=26):
    sq = RoundedRectangle(corner_radius=0.09, width=size, height=size, stroke_color=color, stroke_width=3,
                          fill_color=ManimColor(BG).interpolate(ManimColor(color), 0.2), fill_opacity=1)
    g = VGroup(sq)
    if label != "":
        g.add(M(str(label), fs, color).move_to(sq))
    return g


def strip(n, color, size=0.5, gap=0.08, odd=None, odd_color=RED, labels=False):
    """Row of n plain tiles; tile index `odd` (0-based) gets odd_color."""
    tiles = [tile(i + 1 if labels else "", odd_color if i == odd else color, size, 24) for i in range(n)]
    return VGroup(*tiles).arrange(RIGHT, buff=gap)


def timeline(y, x0=-2.2, x1=6.1):
    return Arrow([x0, y, 0], [x1, y, 0], color=GREY, stroke_width=3, buff=0, max_tip_length_to_length_ratio=0.04)


class ProfileScene(SpokenScene):
    def add_inset(self):
        img, frame, cap, tag, rule = inset_group()
        self.add(img, frame, cap, tag, rule)


# ----------------------------------------------------------------------------- s00 title
class S00Title(TitleCard):
    LESSON = "Scientist profile"
    TITLE = "Linus Pauling"

    def construct(self):
        img, frame = portrait_pair(4.7)
        grp = Group(img, frame)
        grp.move_to([-3.3, 0.35, 0])
        cap = caption_under(frame, size=24).shift(DOWN * 0.15)
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        name = T(self.TITLE, size=54, font=TITLE_FONT)
        dates = T("1901–1994", size=38, color=GOLD)
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


# ----------------------------------------------------------------------------- s01 1949, the electrophoresis run
class S011949(ProfileScene):
    def construct(self):
        self.add_inset()
        ay = 2.6
        axis = timeline(ay)
        dot = Dot([-1.2, ay, 0], radius=0.12, color=GOLD)
        date = T("1949", 36, GOLD, weight=BOLD).next_to(dot, UP, buff=0.22)
        self.at("1949")
        self.play(Create(axis), FadeIn(dot, scale=2), FadeIn(date, shift=UP * 0.1), run_time=0.6)

        # the four people
        ny = 1.3
        pauling = lab("Pauling", TEAL, 24)
        itano = lab(["Harvey Itano", "physician"], TEXT, 24)
        singer = lab(["S. J. Singer", "researcher"], TEXT, 24)
        wells = lab(["Ibert Wells", "researcher"], TEXT, 24)
        row = VGroup(pauling, itano, singer, wells).arrange(RIGHT, buff=0.18)
        fit(row, max_w=8.6)
        row.move_to([PANEL_C, ny, 0])
        self.at("Pauling")
        self.play(pop(pauling), run_time=0.4)
        self.at("physician")
        self.play(pop(itano), run_time=0.4)
        self.at("Singer")
        self.play(pop(singer), run_time=0.4)
        self.at("Ibert Wells")
        self.play(pop(wells), run_time=0.4)

        # the cell: a channel with two lanes
        frame_box = RoundedRectangle(corner_radius=0.2, width=8.5, height=3.15, stroke_color=YELLOW, stroke_width=3,
                                     fill_color=YELLOW, fill_opacity=0.05).move_to([PANEL_C, -1.6, 0])
        cell_lab = T("electrophoresis cell", 26, YELLOW).move_to([PANEL_C, 0.32, 0])
        left = frame_box.get_left()[0] + 0.3
        healthy = lab("healthy hemoglobin", GREEN, 24)
        sickle = lab("sickle-cell hemoglobin", RED, 24)
        healthy.move_to([left + healthy.width / 2, -0.75, 0])
        sickle.move_to([left + sickle.width / 2, -1.7, 0])
        self.at("ran")
        self.play(Create(frame_box), run_time=0.6)
        self.at("healthy")
        self.play(pop(healthy), run_time=0.4)
        self.at("sickle cell hemoglobin")
        self.play(pop(sickle), run_time=0.4)
        self.at("electrophoresis")
        self.play(FadeIn(cell_lab, shift=UP * 0.1), run_time=0.4)

        # drift at different speeds: ghosts mark the start
        x_start = left - 0.12
        start = DashedLine([x_start, -0.2, 0], [x_start, -2.95, 0], color=GREY, stroke_width=2.5, dash_length=0.12)
        start_lab = T("start", 22, GREY).move_to([x_start + 0.5, -2.6, 0])
        trail_h = always_redraw(lambda: Line([x_start, healthy.get_center()[1], 0], healthy.get_left() + LEFT * 0.03,
                                             color=GREEN, stroke_width=4).set_opacity(0.7))
        trail_s = always_redraw(lambda: Line([x_start, sickle.get_center()[1], 0], sickle.get_left() + LEFT * 0.03,
                                             color=RED, stroke_width=4).set_opacity(0.7))
        self.at("drift", lead=0.3)
        self.add(start, start_lab, trail_h, trail_s)
        self.play(healthy.animate.shift(RIGHT * 3.1), sickle.animate.shift(RIGHT * 1.5),
                  run_time=2.2, rate_func=linear)

        # extra positive charge on the sickle protein
        tag = lab("+ extra positive charge", RED, 24).move_to([sickle.get_center()[0] + 0.6, -2.65, 0])
        self.at("extra")
        self.play(pop(tag), Indicate(sickle, color=RED, scale_factor=1.05), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- s02 a molecular disease
class S02Disease(ProfileScene):
    def construct(self):
        self.add_inset()
        n = 7
        # row A: healthy; row B: sickle, one tile different
        la = lab("healthy hemoglobin", GREEN, 24)
        lb = lab("sickle-cell hemoglobin", RED, 24)
        sa = strip(n, GREEN, 0.5)
        sb = strip(n, GREEN, 0.5, odd=5, odd_color=RED)
        lb.move_to([-2.3 + lb.width / 2, 1.3, 0])
        la.move_to([-2.3 + la.width / 2, 2.4, 0])
        sa.move_to([lb.get_right()[0] + 0.3 + sa.width / 2, 2.4, 0])
        sb.move_to([lb.get_right()[0] + 0.3 + sb.width / 2, 1.3, 0])
        self.at("two molecules", lead=0.0)
        self.play(pop(la), FadeIn(sa, lag_ratio=0.1), run_time=0.5)
        self.play(pop(lb), FadeIn(sb, lag_ratio=0.1), run_time=0.5)

        odd = sb[5]
        one = lab("one letter", RED, 24)
        one.next_to(odd, DOWN, buff=0.35)
        pointer = Line(one.get_top(), odd.get_bottom() + DOWN * 0.04, color=RED, stroke_width=3)
        self.at("letter")
        self.play(Create(pointer), pop(one), Indicate(odd, color=RED, scale_factor=1.3), run_time=0.7)

        # red cell -> crescent
        disc = Circle(radius=0.8, color=GREEN, stroke_width=4, fill_color=GREEN, fill_opacity=0.25)
        disc.move_to([PANEL_C, -1.0, 0])
        disc_lab = T("red cell", 26, GREEN).next_to(disc, DOWN, buff=0.3)
        crescent = Difference(Circle(radius=0.9), Circle(radius=0.8).shift(RIGHT * 0.34 + UP * 0.06))
        crescent.set_stroke(RED, 4).set_fill(RED, 0.35).rotate(-0.5).move_to(disc)
        cres_lab = T("crescent", 26, RED).next_to(disc, DOWN, buff=0.3)
        self.at("red cells")
        self.play(FadeIn(disc, scale=0.7), FadeIn(disc_lab), run_time=0.5)
        self.at("crescents", lead=0.5)
        self.play(Transform(disc, crescent), Transform(disc_lab, cres_lab), run_time=0.8)
        self.wait(0.3)

        # phase 2: the phrase
        upper = VGroup(la, sa, lb, sb, one, pointer, disc, disc_lab)
        self.at("named it", lead=0.3)
        self.play(FadeOut(upper), run_time=0.5)
        phrase = T("“a molecular disease”", 48, TEAL, font=TITLE_FONT).move_to([PANEL_C, 2.5, 0])
        self.at("molecular disease", lead=0.3)
        self.play(FadeIn(phrase, shift=UP * 0.15), run_time=0.6)
        first = lab("the first time", GOLD, 28).move_to([PANEL_C, 1.45, 0])
        self.at("first time", lead=0.3)
        self.play(pop(first), run_time=0.4)

        ill = lab("a specific human illness", RED, 26)
        dfc = lab("a specific defect", RED, 26)
        mol = lab("in a specific molecule", CHAIN, 26)
        chain = VGroup(ill, dfc, mol).arrange(DOWN, buff=0.5).move_to([PANEL_C, -1.15, 0])
        a1 = Arrow(ill.get_bottom(), dfc.get_top(), color=TEXT, buff=0.06, stroke_width=4, max_tip_length_to_length_ratio=0.35)
        a2 = Arrow(dfc.get_bottom(), mol.get_top(), color=TEXT, buff=0.06, stroke_width=4, max_tip_length_to_length_ratio=0.35)
        self.at("human illness")
        self.play(pop(ill), run_time=0.4)
        self.at("defect")
        self.play(GrowArrow(a1), pop(dfc), run_time=0.5)
        self.at("specific molecule", lead=0.3)
        self.play(GrowArrow(a2), pop(mol), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s03 Ingram, then the leap
class S03Ingram(ProfileScene):
    def construct(self):
        self.add_inset()
        ay = 2.7
        axis = timeline(ay)
        d49 = Dot([-1.2, ay, 0], radius=0.1, color=GOLD)
        l49 = T("1949", 28, GOLD).next_to(d49, UP, buff=0.18).set_opacity(0.6)
        d_later = Dot([2.8, ay, 0], radius=0.12, color=GOLD)
        l_later = T("later", 32, GOLD, weight=BOLD).next_to(d_later, UP, buff=0.2)
        self.add(axis, d49, l49)
        ingram = lab("Vernon Ingram", TEXT, 26).move_to([2.8, 1.75, 0])
        self.at("Vernon", lead=0.0)
        self.play(pop(ingram), run_time=0.45)
        l_link = Line(d_later.get_center(), ingram.get_top(), color=GOLD, stroke_width=2.5)
        self.at("later")
        self.play(FadeIn(d_later, scale=2), Create(l_link), FadeIn(l_later, shift=UP * 0.1), run_time=0.5)

        # the beta chain strip, position 6 flagged
        beta = strip(6, CHAIN, 0.62, 0.08, labels=True)
        beta.move_to([-0.15, 0.4, 0])
        beta_lab = T("β chain", 28, CHAIN).next_to(beta, UP, buff=0.3).align_to(beta, LEFT)
        self.at("exact lesion", lead=0.1)
        self.play(FadeIn(beta, lag_ratio=0.12), run_time=0.9)

        glu = lab("glutamate", GREEN, 26)
        val = lab("valine", RED, 26)
        arr = Arrow(LEFT * 0.4, RIGHT * 0.4, color=TEXT, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.45)
        swap = VGroup(glu, arr, val).arrange(RIGHT, buff=0.22).move_to([beta[5].get_center()[0], -0.85, 0])
        self.at("glutamate", lead=0.3)
        self.play(pop(glu), run_time=0.4)
        self.at("valine", lead=0.3)
        self.play(GrowArrow(arr), pop(val), run_time=0.5)

        six = beta[5]
        hot = tile(6, RED, 0.62, 26).move_to(six)
        link = Line(six.get_bottom(), swap.get_top() + UP * 0.02, color=RED, stroke_width=3)
        self.at("position 6", lead=0.3)
        self.play(Transform(six, hot), Create(link), run_time=0.6)
        self.at("chain", lead=0.3)
        self.play(FadeIn(beta_lab), run_time=0.4)

        slide = lab("sickle-cell slide", GREY, 24).move_to([4.7, 0.4, 0])
        sl_link = Line(six.get_right(), slide.get_left(), color=GREY, stroke_width=2.5)
        self.at("the very mutation", lead=0.3)
        self.play(Create(sl_link), run_time=0.3)
        self.at("sickle cell slide", lead=0.5)
        self.play(pop(slide), run_time=0.45)

        # the conceptual leap
        leap = lab(["Pauling’s", "conceptual leap"], TEAL, 24)
        drug = lab(["every", "mutation-targeted drug"], YELLOW, 24)
        drug.move_to([6.2 - drug.width / 2, -2.3, 0])
        leap.move_to([-2.3 + leap.width / 2, -2.3, 0])
        arrow2 = Arrow(leap.get_right() + RIGHT * 0.05, drug.get_left() - RIGHT * 0.05, color=TEXT, buff=0,
                       stroke_width=4, max_tip_length_to_length_ratio=0.4)
        self.at("conceptual leap", lead=0.3)
        self.play(pop(leap), run_time=0.45)
        self.at("every mutation", lead=0.3)
        self.play(GrowArrow(arrow2), pop(drug), run_time=0.55)
        phrase = lab(["“a molecular", "disease”"], TEAL, 24)
        phrase.move_to(leap)
        self.at("that one phrase", lead=0.3)
        arrow3 = Arrow(phrase.get_right() + RIGHT * 0.05, drug.get_left() - RIGHT * 0.05, color=TEAL, buff=0,
                       stroke_width=4, max_tip_length_to_length_ratio=0.3)
        self.play(Transform(leap, phrase), Transform(arrow2, arrow3), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- s04 the helix remark
class S04Helix(ProfileScene):
    def construct(self):
        self.add_inset()
        ay = 2.65
        axis = timeline(ay)
        d48 = Dot([-1.2, ay, 0], radius=0.12, color=GOLD)
        l48 = T("1948", 36, GOLD, weight=BOLD).next_to(d48, UP, buff=0.22)
        d49 = Dot([3.2, ay, 0], radius=0.1, color=GOLD)
        l49 = T("1949", 28, GOLD).next_to(d49, UP, buff=0.18).set_opacity(0.6)
        md = T("“a molecular disease”", 24, TEAL).next_to(d49, DOWN, buff=0.25).set_opacity(0.8)
        md.shift(LEFT * 0.0)
        self.add(axis, d49, l49)
        self.add(md)

        remark = lab("alpha-helix remark", TEAL, 28).move_to([-0.4, 1.35, 0])
        self.at("alpha helix", lead=0.1)
        self.play(pop(remark), run_time=0.45)

        bed = lab("sickbed", RED, 26)
        ox = lab("Oxford", PLACE, 26)
        pair = VGroup(bed, ox).arrange(RIGHT, buff=0.3).move_to([-0.4, 0.3, 0])
        self.at("sick bed", lead=0.2)
        self.play(pop(bed), run_time=0.4)
        self.at("Oxford", lead=0.2)
        self.play(pop(ox), run_time=0.4)
        self.at("1948", lead=0.3)
        self.play(FadeIn(d48, scale=2), FadeIn(l48, shift=UP * 0.1), run_time=0.5)

        # the same habit: behavior -> structure
        beh = lab("behavior", YELLOW, 28)
        stru = lab("structure", CHAIN, 28)
        hab_arrow = Arrow(LEFT * 0.7, RIGHT * 0.7, color=TEXT, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3)
        habit = VGroup(stru, hab_arrow, beh).arrange(RIGHT, buff=0.3)
        # reading structure OFF behavior: the arrow points from behavior to structure
        habit = VGroup(beh, hab_arrow, stru).arrange(RIGHT, buff=0.3).move_to([PANEL_C - 0.2, -1.55, 0])
        same = T("the same habit", 28, GOLD).next_to(habit, UP, buff=0.3)
        self.at("same habit", lead=0.3)
        self.play(FadeIn(same, shift=UP * 0.1), run_time=0.4)
        self.at("structure", lead=0.3, nth=0)
        self.play(pop(stru), run_time=0.4)
        self.at("behavior", lead=0.3)
        self.play(pop(beh), GrowArrow(hab_arrow), run_time=0.5)

        # the quote beats: pleased with this structure; late in the night; pondering
        self.at("pleased", lead=0.2)
        self.play(Indicate(stru, color=CHAIN, scale_factor=1.12), run_time=0.8)
        moon = Difference(Circle(radius=0.42), Circle(radius=0.38).shift(RIGHT * 0.22 + UP * 0.08))
        moon.set_stroke(GREY, 3).set_fill(GREY, 0.5).rotate(0.4).move_to([-0.3, -2.75, 0])
        ponder = T("pondering", 28, GREY, slant=ITALIC).next_to(moon, RIGHT, buff=0.35)
        self.at("late in the night", lead=0.3)
        self.play(FadeIn(moon, scale=0.6), run_time=0.5)
        self.at("pondering", lead=0.2)
        self.play(FadeIn(ponder, shift=RIGHT * 0.1), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s05 quote (silent)
class S05Quote(ProfileScene):
    def construct(self):
        self.add_inset()
        words = [T(w, 56, TEXT, font=TITLE_FONT) for w in ["“a", "molecular", "disease”"]]
        q = VGroup(*words).arrange(RIGHT, buff=0.3)
        fit(q, max_w=8.4)
        who = T("— Linus Pauling", 32, GOLD)
        g = VGroup(q, who).arrange(DOWN, aligned_edge=RIGHT, buff=0.7).move_to([PANEL_C, 0.1, 0])
        under = Line(q.get_left() + DOWN * 0.55, q.get_right() + DOWN * 0.55, color=TEAL, stroke_width=4)
        under.move_to(q.get_center() + DOWN * 0.62)
        for w in words:
            w.set_opacity(0)
        who.set_opacity(0)
        self.add(q, who)
        self.wait(0.3)
        for w in words:
            self.play(w.animate.set_opacity(1.0), run_time=0.7)
        self.play(Create(under), run_time=0.7)
        self.wait(0.3)
        self.play(who.animate.set_opacity(1.0), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s06 end card
class S06End(EndCard):
    LINE = "Coined “molecular disease” from hemoglobin’s charge difference; earlier deduced the alpha helix."

    def construct(self):
        a = T("Coined “molecular disease” from hemoglobin’s charge difference;", size=40, font=TITLE_FONT)
        b = T("earlier deduced the alpha helix.", size=40, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.22)
        fit(line, max_w=12.2)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
