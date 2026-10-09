"""Linus Pauling: a scientist profile (Biochemistrypedia, amino-acids lesson).

Narration is the lesson entry's `story`, verbatim (1,199 characters, five scenes cut at sentence
boundaries). Everything on screen comes from that entry (name, dates, contribution, story, quotes).
The portrait is an AI-generated engraving-style illustration from The Molecule Hunters; it is
captioned "illustration · AI-generated" whenever it is on screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = time and Pauling: name/dates, timeline markers, "the first time", the Nobel Prizes, "Pauling's"
  TEAL   = Pauling's chemistry: the chain/strip, the coil, the alpha helix, "molecular disease", the DNA proposal
  YELLOW = tools and data: paper, slide rule, electrophoresis apparatus, the photographs
  RED    = what went wrong or stood in the way: infection, the old assumption, sickle-cell, the lesion,
           "wrong", the passport
  GREEN  = healthy hemoglobin (this film uses no hydrogen-bond arrows)
  PLACE (lavender) = places and institutions: Oxford, the government, King's College
  GREY   = axes, de-emphasized things
No molecular structure is drawn: the chain is a strip of numbered residue tiles, the coil is an end-on
arrangement of those tiles, sickle/healthy hemoglobin are colored spots on an apparatus schematic, and
the beta chain is a row of plain boxes.
"""
import math

import numpy as np
from bp_style import *  # noqa: F401,F403

PORTRAIT = "/Users/deppmann/biochempedia/public/scientists/linus-pauling.png"
CAPTION = "illustration · AI-generated"
PLACE = "#B39DDB"       # places and institutions

# left column (portrait inset + name), right panel (the story animates here)
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


class ProfileScene(SpokenScene):
    """SpokenScene that starts with the inset (portrait + name) already on screen."""

    def add_inset(self):
        img, frame, cap, tag, rule = inset_group()
        self.add(img, frame, cap, tag, rule)
        self.inset_frame = frame


def tile(n, color=TEAL, size=0.62, fs=26):
    sq = RoundedRectangle(corner_radius=0.09, width=size, height=size, stroke_color=color, stroke_width=3,
                          fill_color=ManimColor(BG).interpolate(ManimColor(color), 0.2), fill_opacity=1)
    return VGroup(sq, M(str(n), fs, color).move_to(sq))


def blank_tile(color=TEAL, size=0.8):
    return RoundedRectangle(corner_radius=0.1, width=size, height=size, stroke_color=color, stroke_width=3,
                            fill_color=ManimColor(BG).interpolate(ManimColor(color), 0.2), fill_opacity=1)


def cross_at(pt, r=0.25, color=RED, w=8):
    return VGroup(Line([-r, -r, 0], [r, r, 0]), Line([-r, r, 0], [r, -r, 0])).set_color(color).set_stroke(width=w) \
        .move_to(pt)


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


# ----------------------------------------------------------------------------- s01 Oxford, the helix
class S01OxfordHelix(ProfileScene):
    N = 8
    CENTER = np.array([4.0, 0.1, 0.0])

    def wheel_pos(self, n):
        """Residue n (1-based) seen end-on: 100 deg per residue = 3.6 per turn, clockwise, spiralling inward
        (the chain running away from the viewer = a right-handed coil)."""
        ang = math.radians(90 - 360 / 3.6 * (n - 1))
        r = 1.85 - 0.08 * (n - 1)
        return self.CENTER + np.array([r * math.cos(ang), r * math.sin(ang), 0.0]), 1.0 - 0.012 * (n - 1)

    def construct(self):
        self.add_inset()
        N = self.N

        # ---- the bedroom: timeline, Oxford, infection, wife -> paper + slide rule
        axis_y = 2.3
        axis = Arrow([-2.2, axis_y, 0], [6.1, axis_y, 0], color=GREY, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.04)
        dot = Dot([-1.2, axis_y, 0], radius=0.12, color=GOLD)
        date = T("March 1948", 36, GOLD, weight=BOLD).next_to(dot, UP, buff=0.22, aligned_edge=LEFT).shift(LEFT * 0.3)
        oxford = lab("Oxford", PLACE, 30)
        oxford.next_to(date, RIGHT, buff=0.7).align_to(date, DOWN).shift(DOWN * 0.04)
        sinus = lab("sinus infection", RED, 30).move_to([0.6, 0.7, 0])
        wife = lab("his wife", TEXT, 30).move_to([-0.1, -1.2, 0])
        arrow = Arrow(wife.get_right() + RIGHT * 0.1, [1.75, -1.2, 0], color=TEXT, stroke_width=4, buff=0,
                      max_tip_length_to_length_ratio=0.3)
        paper = lab("paper", YELLOW, 30).move_to([3.0, -1.2, 0])
        rule_chip = lab("slide rule", YELLOW, 30).move_to([5.15, -1.2, 0])

        self.play(Create(axis), run_time=0.6)
        self.at("sinus infection")
        self.play(pop(sinus), run_time=0.45)
        self.at("Oxford")
        self.play(pop(oxford), run_time=0.45)
        self.at("March 1948")
        self.play(FadeIn(dot, scale=2), FadeIn(date, shift=UP * 0.1), run_time=0.6)
        self.play(Indicate(date, color=GOLD, scale_factor=1.1), run_time=0.8)
        self.at("asked his wife")
        self.play(pop(wife), run_time=0.45)
        self.at("bring him")
        self.play(GrowArrow(arrow), run_time=0.4)
        self.at("paper")
        self.play(pop(paper), run_time=0.4)
        self.at("slide rule")
        self.play(pop(rule_chip), run_time=0.4)

        # ---- the chain on an ordinary sheet
        sheet = RoundedRectangle(corner_radius=0.16, width=7.4, height=2.3, stroke_color=YELLOW, stroke_width=3,
                                 fill_color=YELLOW, fill_opacity=0.07).move_to([PANEL_C, 1.2, 0])
        sheet_lab = T("an ordinary sheet", 26, YELLOW).move_to([PANEL_C, -0.3, 0])
        xs = [PANEL_C + (i - 3.5) * 0.9 for i in range(N)]
        tiles = [tile(i + 1) for i in range(N)]
        for t, x in zip(tiles, xs):
            t.move_to([x, 1.2, 0]).set_z_index(3)
        w = ValueTracker(3.0)
        links = VGroup(*[
            always_redraw(lambda a=tiles[i], b=tiles[i + 1]: Line(
                a.get_center(), b.get_center(), color=TEAL, stroke_width=w.get_value(),
                stroke_opacity=min(a[0].get_stroke_opacity(), b[0].get_stroke_opacity())).set_z_index(1))
            for i in range(N - 1)
        ])
        chain_lab = T("polypeptide chain", 32, TEAL).move_to([PANEL_C, 2.85, 0])

        self.at("drew a polypeptide", lead=0.2)
        self.play(FadeOut(VGroup(axis, dot, date, oxford, sinus, wife, arrow, rule_chip)),
                  FadeOut(paper[1]), Transform(paper[0], sheet), run_time=0.5)
        self.at("polypeptide chain")
        self.add(links)
        self.play(FadeIn(chain_lab, shift=UP * 0.1),
                  LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.2), run_time=1.2)
        self.at("ordinary sheet")
        self.play(FadeIn(sheet_lab, shift=UP * 0.1), run_time=0.5)

        # ---- fold: the strip winds up into an end-on coil
        targets = []
        for i, t in enumerate(tiles):
            pos, sc = self.wheel_pos(i + 1)
            targets.append(Transform(t, t.copy().scale(sc).move_to(pos), path_arc=-1.4))
        spiral = ParametricFunction(
            lambda s: self.CENTER + np.array([
                (1.85 - 0.08 * (s - 1)) * math.cos(math.radians(90 - 100 * (s - 1))),
                (1.85 - 0.08 * (s - 1)) * math.sin(math.radians(90 - 100 * (s - 1))), 0]),
            t_range=[1, N, 0.02], color=TEAL, stroke_width=4).set_z_index(1).set_fill(opacity=0).set_stroke(opacity=0.6)
        self.at("folded")
        self.play(FadeOut(paper[0]), FadeOut(sheet_lab), FadeOut(chain_lab),
                  LaggedStart(*targets, lag_ratio=0.1), w.animate.set_value(4), run_time=1.2)
        for l in links:
            l.clear_updaters()
        endon = T("seen end-on, down the coil", 24, GREY).move_to(self.CENTER + DOWN * 2.45)
        self.play(FadeOut(links), FadeIn(spiral), FadeIn(endon), run_time=0.3)

        coil = lab(["right-handed", "coil"], TEAL, 30).move_to([-0.3, 1.6, 0])
        turn_arrow = Arc(radius=0.7, start_angle=math.radians(90), angle=-math.radians(260), color=TEAL,
                         stroke_width=5).add_tip(tip_length=0.22).move_arc_center_to(self.CENTER)
        self.at("coil")
        self.play(pop(coil), Create(turn_arrow), run_time=0.7)

        # 3.6 residues per turn: a hand sweeps one full turn; the counter reads residues advanced (angle / 100 deg)
        per_turn = lab(["3.6 residues", "per turn"], TEAL, 30).move_to([-0.3, 0.0, 0])
        v = ValueTracker(0.0)

        def sweep():
            a = v.get_value()
            arc = Arc(radius=0.92, start_angle=math.radians(90), angle=-math.radians(max(a, 0.01)),
                      arc_center=self.CENTER, color=TEXT, stroke_width=4)
            ang = math.radians(90 - a)
            u = np.array([math.cos(ang), math.sin(ang), 0.0])
            hand = Line(self.CENTER + u * 0.8, self.CENTER + u * 1.04, color=TEXT, stroke_width=5)
            return VGroup(arc, hand)

        dial = always_redraw(sweep)
        counter = always_redraw(lambda: M(f"{v.get_value() / 100:.1f}", 44, TEAL).move_to(self.CENTER))
        self.at("3 6 residues")
        self.play(FadeOut(turn_arrow), pop(per_turn), run_time=0.4)
        self.add(dial, counter)
        self.play(v.animate.set_value(360), run_time=1.2, rate_func=smooth)
        dial.clear_updaters()
        counter.clear_updaters()

        helix_chip = lab("alpha helix", TEAL, 38).move_to([-0.3, -1.7, 0])
        self.at("alpha helix")
        self.play(pop(helix_chip), FadeOut(dial), run_time=0.5)
        self.play(Indicate(helix_chip, color=TEAL, scale_factor=1.08), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- s02 not a whole number
class S02WholeNumber(ProfileScene):
    def construct(self):
        self.add_inset()
        helix = lab("alpha helix", TEAL, 32).move_to([-0.1, 2.3, 0])
        assume = lab(["the assumption", "everyone else clung to"], RED, 28).move_to([4.0, 2.3, 0])
        self.at("cracked it")
        self.play(pop(helix), run_time=0.45)
        self.at("assumption")
        self.play(pop(assume), run_time=0.5)
        self.at("clung to")
        self.play(Indicate(assume, color=RED, scale_factor=1.08), run_time=0.7)

        # number line: whole numbers of amino acids per turn
        x0, k, v0 = -1.4, 2.6, 2.5
        X = lambda v: x0 + (v - v0) * k
        ay = 0.1
        base = Line([X(2.5), ay, 0], [X(5.5), ay, 0], color=GREY, stroke_width=3)
        ticks = VGroup(*[Line([X(v), ay - 0.12, 0], [X(v), ay + 0.12, 0], color=GREY, stroke_width=3) for v in (3, 4, 5)])
        nums = VGroup(*[T(str(v), 28, GREY).move_to([X(v), ay - 0.5, 0]) for v in (3, 4, 5)])
        title = T("amino acids per turn", 26, GREY).move_to([PANEL_C, ay - 1.75, 0])
        self.at("the coil had to close")
        self.play(Create(base), FadeIn(ticks), FadeIn(nums), run_time=0.8)
        reds = VGroup(*[Dot([X(v), ay, 0], radius=0.17, color=RED) for v in (3, 4, 5)])
        whole = T("a whole number", 30, RED).move_to([PANEL_C, ay - 1.1, 0])
        self.at("whole number")
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in reds], lag_ratio=0.2), FadeIn(whole, shift=DOWN * 0.1),
                  run_time=0.8)
        self.at("amino acids")
        self.play(FadeIn(title), run_time=0.5)

        # the helix was not on a whole number
        mark = Dot([X(3.6), ay, 0], radius=0.2, color=TEAL).set_z_index(3)
        lab36 = M("3.6", 34, TEAL).move_to([X(3.6), ay + 0.85, 0])
        self.at("acids", lead=-0.2)
        strike = Line(assume.get_corner(DL) + RIGHT * 0.05, assume.get_corner(UR) - RIGHT * 0.05, color=RED, stroke_width=5)
        self.play(Create(strike), assume.animate.set_opacity(0.55), 
                  FadeIn(mark, scale=2.5), FadeIn(lab36, shift=DOWN * 0.1), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s03 Itano, electrophoresis
class S03Itano(ProfileScene):
    def construct(self):
        self.add_inset()
        ay = 2.45
        axis = Arrow([-2.2, ay, 0], [6.15, ay, 0], color=GREY, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.04)
        d1, d2 = Dot([-1.2, ay, 0], radius=0.12, color=GOLD), Dot([3.6, ay, 0], radius=0.12, color=GOLD)
        l1 = T("March 1948", 30, GOLD, weight=BOLD)
        l1.move_to([-2.0 + l1.width / 2, ay + 0.5, 0]).set_opacity(0.6)
        l2 = T("the following year", 30, GOLD, weight=BOLD).move_to([3.6, ay + 0.5, 0])
        self.at("following year")
        self.play(Create(axis), FadeIn(d1), FadeIn(l1), FadeIn(d2, scale=2), FadeIn(l2, shift=UP * 0.1), run_time=0.7)
        itano = lab("working with Harvey Itano", TEXT, 28).move_to([3.6, 1.4, 0])
        self.at("Harvey Itano")
        self.play(pop(itano), run_time=0.5)

        sick = lab(["sickle-cell", "hemoglobin"], RED, 26).move_to([-1.0, 0.8, 0])
        heal = lab(["healthy", "hemoglobin"], GREEN, 26).move_to([-1.0, -0.8, 0])
        self.play(Indicate(itano, color=TEXT, scale_factor=1.06), run_time=0.7)
        self.at("sickle cell")
        self.play(pop(sick), run_time=0.45)
        self.at("healthy hemoglobin")
        self.play(pop(heal), run_time=0.45)

        # electrophoresis: schematic apparatus, two lanes
        tank = RoundedRectangle(corner_radius=0.2, width=5.4, height=3.2, stroke_color=YELLOW, stroke_width=3,
                                fill_color=YELLOW, fill_opacity=0.06).move_to([3.45, 0.0, 0])
        lane_a = Line([0.95, 0.8, 0], [5.95, 0.8, 0], color=GREY, stroke_width=2).set_opacity(0.6)
        lane_b = Line([0.95, -0.8, 0], [5.95, -0.8, 0], color=GREY, stroke_width=2).set_opacity(0.6)
        start = DashedLine([1.3, 1.35, 0], [1.3, -1.35, 0], color=GREY, stroke_width=2, dash_length=0.1)
        tank_lab = T("electrophoresis", 30, YELLOW, weight=BOLD).move_to([3.45, 2.1, 0])
        sp_a = Dot([1.3, 0.8, 0], radius=0.18, color=RED)
        sp_b = Dot([1.3, -0.8, 0], radius=0.18, color=GREEN)
        self.at("healthy hemoglobin", lead=-0.5)      # let the second chip land before the apparatus replaces the timeline
        self.play(FadeOut(VGroup(axis, d1, d2, l1, l2, itano)), run_time=0.3)
        self.at("electrophoresis")
        self.play(FadeIn(tank), Create(lane_a), Create(lane_b), Create(start), FadeIn(tank_lab, shift=UP * 0.1),
                  run_time=0.7)
        self.play(FadeIn(sp_a, scale=2), FadeIn(sp_b, scale=2), run_time=0.4)

        xa, xb = 2.9, 5.5
        self.at("drift")
        ga = DashedLine([xa, 0.62, 0], [xa, -2.0, 0], color=RED, stroke_width=3, dash_length=0.1)
        gb = DashedLine([xb, -0.98, 0], [xb, -2.0, 0], color=GREEN, stroke_width=3, dash_length=0.1)
        gap = DoubleArrow([xa, -2.0, 0], [xb, -2.0, 0], color=TEXT, stroke_width=4, buff=0, tip_length=0.14)
        speeds = T("different speeds", 30, TEXT, weight=BOLD).move_to([(xa + xb) / 2, -2.55, 0])
        self.play(
            AnimationGroup(sp_a.animate.move_to([xa, 0.8, 0]), sp_b.animate.move_to([xb, -0.8, 0]),
                           run_time=1.5, rate_func=linear),
            Succession(Wait(0.45), AnimationGroup(Create(ga), Create(gb), GrowFromCenter(gap),
                                                  FadeIn(speeds, shift=UP * 0.1), run_time=0.6)),
        )
        # the first time: illness -> defect -> molecule
        stage = VGroup(sick, heal, tank, lane_a, lane_b, start, tank_lab, sp_a, sp_b, ga, gb, gap, speeds)
        first = lab("the first time", GOLD, 32).move_to([PANEL_C, 2.6, 0])
        ill = lab("a specific human illness", RED, 30).move_to([PANEL_C, 1.3, 0])
        dfc = lab("a specific defect", RED, 30).move_to([PANEL_C, -0.1, 0])
        mol = lab("in a specific molecule", TEAL, 30).move_to([PANEL_C, -1.5, 0])
        a1 = Arrow(ill.get_bottom(), dfc.get_top(), color=TEXT, stroke_width=5, buff=0.08, tip_length=0.2)
        a2 = Arrow(dfc.get_bottom(), mol.get_top(), color=TEXT, stroke_width=5, buff=0.08, tip_length=0.2)
        self.at("The first time", lead=0.5)
        self.play(FadeOut(stage), run_time=0.4)
        self.at("first time")
        self.play(pop(first), run_time=0.4)
        self.at("specific human illness")
        self.play(pop(ill), run_time=0.45)
        self.at("specific defect")
        self.play(GrowArrow(a1), pop(dfc), run_time=0.5)
        self.at("specific molecule")
        self.play(GrowArrow(a2), pop(mol), run_time=0.5)
        self.play(Indicate(mol, color=TEAL, scale_factor=1.06), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- s04 molecular disease, Ingram
class S04MolecularDisease(ProfileScene):
    def construct(self):
        self.add_inset()
        phrase = lab("“molecular disease”", TEAL, 38).move_to([PANEL_C, 2.2, 0])
        self.at("molecular disease")
        self.play(pop(phrase), run_time=0.5)

        self.play(Indicate(phrase, color=TEAL, scale_factor=1.06), run_time=0.7)
        med = T("reframed medicine", 34, TEXT).move_to([PANEL_C, 1.1, 0])
        arr = Arrow(phrase.get_bottom(), med.get_top() + UP * 0.05, color=TEXT, stroke_width=5, buff=0.06, tip_length=0.2)
        self.at("reframed medicine")
        self.play(GrowArrow(arr), FadeIn(med, shift=UP * 0.1), run_time=0.5)

        # a row of boxes: one amino acid in a chain changes
        xs = [PANEL_C + (i - 2.5) * 1.0 for i in range(6)]
        row = VGroup(*[blank_tile().move_to([x, -0.2, 0]) for x in xs])
        row_lab = T("amino acids", 26, TEAL).move_to([PANEL_C, -0.95, 0])
        more = T("…", 40, TEAL).move_to([xs[5] + 0.85, -0.2, 0])   # the chain goes on: these are not the whole chain
        self.at("single changed")
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.12) for t in row], lag_ratio=0.06), FadeIn(row_lab),
                  FadeIn(more), run_time=0.5)
        bad_tile = blank_tile(RED).move_to(row[5].get_center())
        self.at("changed")
        self.play(Transform(row[5], bad_tile), Flash(row[5].get_center(), color=RED, flash_radius=0.7, line_length=0.15),
                  run_time=0.5)
        cat = T("the whole catastrophe", 36, RED, weight=BOLD).move_to([PANEL_C, -1.9, 0])
        self.at("whole catastrophe")
        self.play(FadeIn(cat, shift=UP * 0.1), Indicate(row[5], color=RED, scale_factor=1.2), run_time=0.7)

        # Vernon Ingram, later: the exact lesion
        ing = lab("Vernon Ingram", TEXT, 30).move_to([1.2, 2.5, 0])
        later = T("later", 30, GOLD, weight=BOLD).move_to([1.2, 1.78, 0])
        self.at("Vernon")
        self.play(FadeOut(VGroup(phrase, arr, med, cat, row_lab)), pop(ing), run_time=0.5)
        self.at("later")
        self.play(FadeIn(later, shift=UP * 0.1), run_time=0.4)

        callout = lab("the exact lesion", RED, 28).move_to([row[5].get_center()[0] - 0.3, 1.05, 0])
        link = Arrow(ing.get_right() + RIGHT * 0.05, callout.get_top() + UP * 0.02, color=TEXT, stroke_width=4, buff=0.05,
                     max_tip_length_to_length_ratio=0.25, path_arc=-0.5)
        self.at("exact lesion")
        self.play(GrowArrow(link), pop(callout), Indicate(row[5], color=RED, scale_factor=1.2), run_time=0.7)

        glu = lab("glutamate", TEAL, 28).move_to(callout.get_center())
        val = lab("valine", RED, 28).move_to(callout.get_center())
        self.at("one glutamate")
        self.play(ReplacementTransform(callout, glu), run_time=0.5)
        self.at("swapped for a valine")
        self.play(ReplacementTransform(glu, val), Flash(val.get_center(), color=RED, flash_radius=0.8, line_length=0.15),
                  run_time=0.6)

        nums = VGroup(*[T(str(i + 1), 26, GREY).move_to([x, -0.85, 0]) for i, x in enumerate(xs)])
        six = Underline(nums[5], color=RED, buff=0.05).set_stroke(width=4)
        self.at("sixth position")
        self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.1) for n in nums], lag_ratio=0.1), Create(six), run_time=0.8)

        brace = Line([xs[0] - 0.4, -1.3, 0], [xs[5] + 1.25, -1.3, 0], color=TEAL, stroke_width=4)
        beta = T("beta chain", 30, TEAL).move_to([brace.get_center()[0], -1.8, 0])
        self.at("beta chain")
        self.play(Create(brace), FadeIn(beta, shift=UP * 0.1), run_time=0.6)

        leap = lab("the conceptual leap", TEAL, 32).move_to([0.6, -2.75, 0])
        self.at("conceptual leap")
        self.play(pop(leap), run_time=0.5)
        paul = T("Pauling's", 38, GOLD, weight=BOLD).next_to(leap, RIGHT, buff=0.4)
        self.at("Pauling's")
        self.play(FadeIn(paul, shift=LEFT * 0.1), Indicate(self.inset_frame, color=GOLD, scale_factor=1.06), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- s05 Nobels, DNA, passport
class S05NobelsDna(ProfileScene):
    def medal(self, x, field):
        ring = Circle(radius=1.3, stroke_color=GOLD, stroke_width=4, fill_color=GOLD, fill_opacity=0.1)
        t = VGroup(T("Nobel", 26, GOLD), T("Prize", 26, GOLD)).arrange(DOWN, buff=0.05)
        t.move_to(ring.get_center() + UP * 0.4)
        f = T(field, 26, TEXT, weight=BOLD).move_to(ring.get_center() + DOWN * 0.45)
        return VGroup(ring, t).move_to([x, 1.8, 0]), f

    def construct(self):
        self.add_inset()
        m1, f1 = self.medal(0.2, "Chemistry")
        m2, f2 = self.medal(3.7, "Peace")
        f1.move_to(m1[0].get_center() + DOWN * 0.45)
        f2.move_to(m2[0].get_center() + DOWN * 0.45)
        unshared = T("unshared", 36, GOLD, weight=BOLD).move_to([PANEL_C, -0.15, 0])
        self.at("two")
        self.play(FadeIn(m1, scale=0.8), FadeIn(m2, scale=0.8), run_time=0.6)
        self.at("unshared")
        self.play(FadeIn(unshared, shift=UP * 0.1), run_time=0.5)
        self.at("Nobel Prizes")
        self.play(Indicate(m1[0], color=GOLD, scale_factor=1.08), Indicate(m2[0], color=GOLD, scale_factor=1.08),
                  run_time=0.7)
        self.at("Chemistry")
        self.play(FadeIn(f1, shift=UP * 0.1), run_time=0.4)
        self.at("Peace")
        self.play(FadeIn(f2, shift=UP * 0.1), run_time=0.4)

        # DNA: a triple helix, wrong
        dna = lab(["Pauling proposed", "a triple helix for DNA"], TEAL, 30).move_to([PANEL_C, 2.2, 0])
        wrong = T("wrong in nearly every particular", 32, RED).move_to([PANEL_C, 0.95, 0])
        self.at("proposed")
        self.play(FadeOut(VGroup(m1, m2, f1, f2, unshared)), run_time=0.4)
        self.play(pop(dna), run_time=0.5)
        self.at("DNA")
        self.play(Indicate(dna, color=TEAL, scale_factor=1.06), run_time=0.7)
        self.at("wrong in nearly")
        self.play(dna[0].animate.set_stroke(RED).set_fill(RED, 0.16), dna[1].animate.set_color(RED),
                  FadeIn(wrong, shift=UP * 0.1), run_time=0.7)

        # the passport, King's College photographs
        gov = lab("the government", PLACE, 28).move_to([-0.2, -0.45, 0])
        pp = lab("passport pulled", RED, 28).move_to([4.5, -0.45, 0])
        arr = Arrow(gov.get_right() + RIGHT * 0.05, pp.get_left() + LEFT * 0.05, color=RED, stroke_width=4, buff=0.0,
                    max_tip_length_to_length_ratio=0.3)
        self.at("particular", lead=0.0)
        self.play(Indicate(wrong, color=RED, scale_factor=1.06), run_time=0.7)
        self.at("partly because", lead=0.0)
        self.play(VGroup(dna, wrong).animate.set_opacity(0.45), run_time=0.4)
        self.at("the government")
        self.play(pop(gov), run_time=0.45)
        self.at("pulled his passport")
        self.play(GrowArrow(arr), pop(pp), run_time=0.5)

        kings = RoundedRectangle(corner_radius=0.2, width=7.4, height=1.3, stroke_color=PLACE, stroke_width=2.5,
                                 fill_color=PLACE, fill_opacity=0.08).move_to([PANEL_C, -2.3, 0])
        k_lab = T("King's College", 30, PLACE).move_to(kings.get_left() + RIGHT * 1.7)
        photos = lab("photographs", YELLOW, 28).move_to([4.2, -2.3, 0])
        blocked = DashedLine(pp.get_bottom() + DOWN * 0.05, [4.5, kings.get_top()[1] + 0.05, 0], color=RED,
                             stroke_width=4, dash_length=0.12)
        x = cross_at(blocked.get_center(), 0.2)
        self.at("never saw")
        self.play(Create(blocked), run_time=0.4)
        self.play(FadeIn(x, scale=1.5), run_time=0.25)
        self.at("photographs")
        self.play(pop(photos), run_time=0.45)
        self.at("King's College")
        self.play(FadeIn(kings), FadeIn(k_lab), run_time=0.5)
        self.play(Indicate(photos, color=YELLOW, scale_factor=1.06), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s06 the quote
class S06Quote(ProfileScene):
    def construct(self):
        self.add_inset()
        lines = ["“I was so pleased with this", "structure that I stayed up until", "late in the night, pondering", "about it.”"]
        q = VGroup(*[T(l, 38, TEXT, font=TITLE_FONT) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        fit(q, max_w=8.4)
        who = T("— Linus Pauling", 32, GOLD)
        g = VGroup(q, who).arrange(DOWN, aligned_edge=RIGHT, buff=0.55).move_to([PANEL_C, 0.1, 0])
        for ln in q:
            ln.set_opacity(0)
        who.set_opacity(0)
        self.add(g)
        self.wait(0.4)
        for ln in q:
            self.play(ln.animate.set_opacity(1.0), run_time=0.8)
        self.wait(0.5)
        self.play(who.animate.set_opacity(1.0), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s07 end card
class S07End(EndCard):
    LINE = "Coined “molecular disease” after pinning sickle-cell anemia on one protein defect."

    def construct(self):
        a = T("Coined “molecular disease” after pinning", size=42, font=TITLE_FONT)
        b = T("sickle-cell anemia on one protein defect.", size=42, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.22)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
