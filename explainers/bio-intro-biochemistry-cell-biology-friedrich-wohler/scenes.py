"""Friedrich Wöhler: a scientist profile (Biochemistrypedia, intro-biochemistry-cell-biology lesson).

Narration is the lesson entry's `story`, verbatim. Everything on screen comes from that entry
(name, dates, contribution, story, quotes). The portrait is an AI-generated engraving-style
illustration from The Molecule Hunters; it is captioned "illustration · AI-generated" whenever it is
on screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = Wöhler himself: name/dates, the portrait frame, his letter and the two quotes
  YELLOW = dates (1828)
  PINK   = the molecules: urea, "molecules of life", the four classes of biomolecules
  TEAL   = Biochemistrypedia brand only (title card, web address)
  GREEN  = living things: the vital force, something already alive, animals' kidneys, living chemistry
  BLUE   = lifeless matter: ordinary matter, the inorganic salt, dead chemistry, the chemistry of everything else
  RED    = the wall and what is blocked or absent: "could not build", the boundary, "no kidney in the room"
  AMBER  = heat under the flask
  LAV    = Berzelius (his mentor)
  GREY   = labels, apparatus outline, the thicket of trees, de-emphasized things
No molecular structure is drawn: the flask is a schematic of the apparatus, the crystals are plain
diamonds, molecules are labelled chips, and the forest is a field of abstract trees.
"""
import math
import random

import numpy as np
from bp_style import *  # noqa: F401,F403

HERE = Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent
PORTRAIT = str(HERE / "wohler_crop.png")   # public/scientists/friedrich-wohler.png cropped to the figure
CAPTION = "illustration · AI-generated"
LAV = "#B39DDB"
PINK = "#EE8FC4"
AMBER = "#E0A458"
NAME = "Friedrich Wöhler"
DATES = "1800–1882"

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
    nm = T(NAME, size=32, font=TITLE_FONT)
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


def xmark(center, color=RED, r=0.24, w=8):
    return VGroup(Line([-r, -r, 0], [r, r, 0]), Line([-r, r, 0], [r, -r, 0])).set_color(color) \
        .set_stroke(width=w).move_to(center)


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


# ----------------------------------------------------------------------------- s01 the vital-force belief
class S01Belief(ProfileScene):
    def construct(self):
        self.add_inset()
        mol = lab("molecules of life", PINK, 32).move_to([0.2, 1.9, 0])
        vital = lab("vital force", GREEN, 26).move_to([4.7, 1.9, 0])
        link = Line(mol.get_right(), vital.get_left(), color=GREEN, stroke_width=4)
        self.at("molecules of life")
        self.play(pop(mol), run_time=0.5)
        self.at("vital force")
        self.play(Create(link), pop(vital), run_time=0.6)

        dead = lab(["ordinary,", "lifeless matter"], BLUE, 26).move_to([-0.3, -1.4, 0])
        up_l = Arrow(dead.get_top() + UP * 0.05, [0.0, mol.get_bottom()[1] - 0.08, 0], color=BLUE, stroke_width=5,
                     buff=0, max_tip_length_to_length_ratio=0.2)
        no = VGroup(T("could not", 24, RED), T("build", 24, RED)).arrange(DOWN, buff=0.05).move_to([1.1, 0.35, 0])
        self.at("could not build")
        self.play(GrowArrow(up_l), FadeIn(no, shift=UP * 0.1), run_time=0.5)
        self.at("ordinary lifeless matter", lead=0.3)
        self.play(pop(dead), run_time=0.5)
        cross = xmark(up_l.point_from_proportion(0.5))
        self.play(FadeIn(cross, scale=1.6), run_time=0.3)

        alive = lab(["something", "already alive"], GREEN, 26).move_to([4.0, -1.4, 0])
        up_r = Arrow(alive.get_top() + UP * 0.05, [1.55, mol.get_bottom()[1] - 0.08, 0], color=GREEN, stroke_width=5,
                     buff=0, max_tip_length_to_length_ratio=0.15)
        borrow = T("borrow", 26, GREEN).move_to([3.95, 0.45, 0])
        self.at("only borrow")
        self.play(GrowArrow(up_r), FadeIn(borrow, shift=UP * 0.1), run_time=0.5)
        self.at("something already alive")
        self.play(pop(alive), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s02 1828: urea from salt
def flask_outline(cx, cy):
    pts = [(-0.3, 1.3), (0.3, 1.3), (0.3, 0.55), (1.15, -0.95), (-1.15, -0.95), (-0.3, 0.55)]
    poly = Polygon(*[[x, y, 0] for x, y in pts], color=GREY, stroke_width=4).round_corners(0.08)
    return poly.move_to([cx, cy, 0])


class S02Urea(ProfileScene):
    def construct(self):
        self.add_inset()
        FX, FY = 0.2, -0.3

        self.at("One afternoon")
        aft = T("one afternoon", 28, GREY).move_to([0.0, 3.05, 0])
        self.play(pop(aft), run_time=0.5)
        self.at("1828")
        yr = M("1828", 44, YELLOW).move_to([2.9, 3.05, 0])
        self.play(Write(yr), run_time=0.5)

        flask = flask_outline(FX, FY)
        self.play(Create(flask), run_time=0.9)

        # liquid inside the flask (absolute coordinates; flask bbox centre is (FX, FY))
        liq_pts = [(-0.52, -0.75), (0.92, -0.75), (1.28, -1.36), (-0.88, -1.36)]
        liquid = Polygon(*[[x, y, 0] for x, y in liq_pts], stroke_width=0, fill_color=BLUE, fill_opacity=0.0)

        heat = VGroup(*[Arrow([x, -2.55, 0], [x, -1.8, 0], color=AMBER, stroke_width=5, buff=0,
                              max_tip_length_to_length_ratio=0.35) for x in (-0.35, 0.2, 0.75)])
        heat_lab = T("heat", 24, AMBER).move_to([1.7, -2.2, 0])
        self.at("heated")
        self.play(LaggedStart(*[GrowArrow(a) for a in heat], lag_ratio=0.25), FadeIn(heat_lab), run_time=0.7)

        salt = lab("inorganic salt", BLUE, 24).move_to([FX, 1.85, 0])
        drop = Arrow(salt.get_bottom() + DOWN * 0.03, [FX, 0.95, 0], color=BLUE, stroke_width=4, buff=0,
                     max_tip_length_to_length_ratio=0.3)
        self.add(liquid)
        self.at("inorganic salt")
        self.play(pop(salt), GrowArrow(drop), liquid.animate.set_fill(BLUE, opacity=0.5), run_time=0.8)

        # crystals appear: the liquid turns to urea
        rnd = random.Random(7)
        spots = [(-0.5, -1.15), (-0.1, -1.0), (0.35, -1.22), (0.75, -1.08), (0.1, -1.28), (-0.7, -1.28),
                 (1.0, -1.28), (0.5, -0.9), (-0.3, -1.3)]
        crystals = VGroup(*[
            Square(side_length=rnd.uniform(0.17, 0.26), stroke_color=PINK, stroke_width=3, fill_color=PINK,
                   fill_opacity=0.55).rotate(rnd.uniform(0.3, 1.2)).move_to([x, y, 0])
            for x, y in spots])
        urea = lab("urea", PINK, 34).move_to([4.3, 1.9, 0])
        self.at("watched")
        self.play(liquid.animate.set_fill(PINK, opacity=0.35), LaggedStart(*[GrowFromCenter(c) for c in crystals],
                                                                           lag_ratio=0.15), run_time=1.1)
        self.at("crystallize")
        self.play(pop(urea), run_time=0.5)
        fl = T("flask", 24, GREY).move_to([1.45, 0.5, 0])
        self.at("his flask")
        self.play(FadeIn(fl), run_time=0.4)

        # the crystals shimmer while the narrator reaches the next sentence
        self.play(LaggedStart(*[Indicate(c, color=PINK, scale_factor=1.35) for c in crystals], lag_ratio=0.12),
                  run_time=1.1)
        self.at("Urea is", lead=0.1)
        self.play(Indicate(urea, color=PINK, scale_factor=1.12), run_time=0.7)

        # what urea is
        waste = T("nitrogen waste", 26, TEXT).move_to([4.3, 1.15, 0])
        self.at("nitrogen waste")
        self.play(pop(waste), run_time=0.5)
        kid = lab("animals' kidneys", GREEN, 28).move_to([4.3, -0.5, 0])
        flush = Arrow([4.3, -0.05, 0], waste.get_bottom() + DOWN * 0.08, color=GREEN, stroke_width=5,
                      buff=0, max_tip_length_to_length_ratio=0.3)
        flush_l = T("flush out", 24, GREEN).move_to([5.6, 0.3, 0])
        self.at("animals flush")
        self.play(GrowArrow(flush), FadeIn(flush_l), run_time=0.6)
        self.at("kidneys", lead=0.25)
        self.play(pop(kid), run_time=0.5)

        # no kidney in the room
        strike = Line(kid.get_left() + RIGHT * 0.06, kid.get_right() - RIGHT * 0.06, color=RED, stroke_width=7)
        none = T("no kidney in the room", 26, RED).move_to([4.45, -1.9, 0])
        self.at("There was no kidney", lead=0.2)
        self.play(Create(strike), kid[0].animate.set_stroke(opacity=0.45), kid[1].animate.set_opacity(0.55),
                  pop(none), run_time=0.6)
        room = DashedVMobject(Rectangle(width=4.3, height=5.5, color=GREY, stroke_width=3), num_dashes=64) \
            .move_to([0.2, -0.25, 0])
        room_l = T("the room", 24, GREY).move_to([-1.1, -2.65, 0])
        self.at("in the room", lead=0.3)
        self.play(Create(room), FadeIn(room_l), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s03 the letter
class S03Letter(ProfileScene):
    def construct(self):
        self.add_inset()
        wo = lab("Wöhler", GOLD, 30).move_to([-0.3, 2.65, 0])
        self.at("He wrote")
        self.play(pop(wo), run_time=0.4)
        bz = lab(["Berzelius", "his mentor"], LAV, 26).move_to([4.6, 2.65, 0])
        arr = Arrow(wo.get_right() + RIGHT * 0.1, bz.get_left() + LEFT * 0.1, color=GOLD, stroke_width=5, buff=0,
                    max_tip_length_to_length_ratio=0.15)
        self.at("his mentor", lead=0.15)
        self.play(GrowArrow(arr), run_time=0.5)
        self.at("Berzelius", lead=0.1)
        self.play(pop(bz), run_time=0.5)

        joke = lab("a joke", GOLD, 28).move_to([0.2, 1.1, 0])
        self.at("a joke")
        self.play(pop(joke), run_time=0.45)
        manif = lab("a manifesto", GREY, 28).move_to([3.9, 1.1, 0])
        self.at("not a manifesto", lead=0.15)
        self.play(pop(manif), run_time=0.45)
        sl = Line(manif.get_left() + RIGHT * 0.08, manif.get_right() - RIGHT * 0.08, color=RED, stroke_width=6)
        self.at("manifesto")
        self.play(Create(sl), manif[0].animate.set_stroke(opacity=0.45), manif[1].animate.set_opacity(0.55), run_time=0.4)

        # the sheet of paper
        paper = RoundedRectangle(corner_radius=0.12, width=8.3, height=2.6,
                                 stroke_color=GOLD, stroke_width=2.5, fill_color=BG, fill_opacity=1)
        paper.set_fill(ManimColor(BG).interpolate(ManimColor(GOLD), 0.07), opacity=1).move_to([PANEL_C, -0.45, 0])
        lines = ["“I can no longer, as it were, hold back", "my chemical urine; and I have to let out",
                 "that I can make urea without needing", "a kidney.”"]
        qs = [T(l, 28, TEXT, font=TITLE_FONT) for l in lines]
        qg = VGroup(*qs).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(paper)
        cues = ["I can no longer", "my chemical urine", "that I can make urea", "a kidney"]
        self.at("I can no longer", lead=0.55)
        self.play(FadeOut(VGroup(joke, manif, sl)), FadeIn(paper), run_time=0.4)
        prev = None
        for i, cue in enumerate(cues):
            self.at(cue, lead=0.1)
            nxt = self.t_of(cues[i + 1]) - 0.1 if i + 1 < len(cues) else self.t_of("The line is irreverent") - 0.15
            ul = Line(qs[i].get_corner(DL) + DOWN * 0.07, qs[i].get_corner(DR) + DOWN * 0.07, color=GOLD,
                      stroke_width=3)
            anims = [FadeIn(qs[i], shift=UP * 0.08, run_time=0.5), Create(ul, run_time=max(0.6, nxt - self.elapsed()),
                                                                         rate_func=linear)]
            if prev is not None:
                anims.append(FadeOut(prev, run_time=0.3))
            self.play(*anims)
            prev = ul
        self.play(FadeOut(prev), run_time=0.2)

        irr = lab("irreverent", GOLD, 28).move_to([0.3, -2.75, 0])
        exact = lab("exact", GOLD, 28).move_to([4.0, -2.75, 0])
        andt = T("and", 24, GREY).move_to([2.15, -2.75, 0])
        self.at("irreverent")
        self.play(pop(irr), run_time=0.5)
        self.at("exact")
        self.play(FadeIn(andt), pop(exact), run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s04 the boundary
class S04Boundary(ProfileScene):
    def construct(self):
        self.add_inset()
        wo = lab("Wöhler", GOLD, 28).move_to([-0.2, 2.5, 0])
        fr = lab("a friend", LAV, 28).move_to([4.2, 2.5, 0])
        self.at("sharing surprise", lead=0.3)
        self.play(pop(wo), run_time=0.4)
        link = Arrow(wo.get_right() + RIGHT * 0.1, fr.get_left() + LEFT * 0.1, color=GOLD, stroke_width=5, buff=0,
                     max_tip_length_to_length_ratio=0.15)
        sup = T("surprise", 28, GOLD, font=TITLE_FONT).move_to([2.0, 3.15, 0])
        self.at("surprise")
        self.play(GrowArrow(link), FadeIn(sup, shift=UP * 0.1), Flash(link.get_center(), color=GOLD, flash_radius=0.4,
                                                                     line_length=0.15), run_time=0.7)
        self.at("a friend", lead=0.1)
        self.play(pop(fr), run_time=0.45)

        # the wall between living and dead chemistry
        liv = lab(["living", "chemistry"], GREEN, 28).move_to([-0.2, -0.7, 0])
        ded = lab(["dead", "chemistry"], BLUE, 28).move_to([4.1, -0.7, 0])
        brick_h = 0.5
        bricks = VGroup(*[Rectangle(width=0.3, height=brick_h - 0.04, stroke_width=2, stroke_color=RED,
                                    fill_color=RED, fill_opacity=0.55).move_to([PANEL_C, 0.95 - brick_h * i, 0])
                          for i in range(9)])
        bricks.move_to([PANEL_C, -0.7, 0])
        self.at("dissolving", lead=0.75)
        self.play(FadeOut(VGroup(wo, fr, link, sup)), run_time=0.3)
        self.play(FadeIn(liv, shift=RIGHT * 0.2), FadeIn(ded, shift=LEFT * 0.2),
                  LaggedStart(*[GrowFromCenter(b) for b in bricks], lag_ratio=0.05), run_time=0.7)
        bound = T("the boundary", 28, RED).move_to([PANEL_C, 2.05, 0])
        self.at("the boundary")
        self.play(pop(bound), run_time=0.4)
        rnd = random.Random(3)
        crumble = [b.animate.shift(np.array([rnd.uniform(-0.5, 0.5), rnd.uniform(-0.7, -0.2), 0])).rotate(rnd.uniform(-1, 1))
                   .set_opacity(0) for b in bricks]
        self.at("had assumed", lead=0.35)
        self.play(LaggedStart(*crumble, lag_ratio=0.08), FadeOut(bound), run_time=1.5)

        # the molecules of life obey the chemistry of everything else
        mol = lab(["molecules", "of life"], PINK, 30).move_to([-0.3, -0.7, 0])
        every = lab(["the chemistry of", "everything else"], BLUE, 30).move_to([4.5, -0.7, 0])
        obey = Arrow(mol.get_right() + RIGHT * 0.1, every.get_left() + LEFT * 0.1, color=TEXT, stroke_width=5,
                     buff=0, max_tip_length_to_length_ratio=0.2)
        obey_l = T("obey", 28, TEXT).next_to(obey, UP, buff=0.12)
        self.at("the molecules of life obey", lead=0.3)
        self.play(ReplacementTransform(liv, mol), ReplacementTransform(ded, every), run_time=0.7)
        self.at("obey", lead=0.2)
        self.play(GrowArrow(obey), FadeIn(obey_l), run_time=0.5)
        self.at("everything else", lead=0.1)
        self.play(Indicate(every, color=BLUE, scale_factor=1.08), Indicate(mol, color=PINK, scale_factor=1.08),
                  run_time=0.9)
        self.finish()


# ----------------------------------------------------------------------------- s05 the forest
def tree(x, y, s=1.0, color=GREY, op=0.55):
    tint = ManimColor(BG).interpolate(ManimColor(color), 0.28)
    crown = Polygon([-0.3 * s, 0.0, 0], [0.3 * s, 0.0, 0], [0.0, 0.8 * s, 0], stroke_width=2.5, stroke_color=color,
                    fill_color=tint, fill_opacity=1)
    trunk = Rectangle(width=0.1 * s, height=0.18 * s, stroke_width=0, fill_color=color, fill_opacity=op)
    trunk.next_to(crown, DOWN, buff=0)
    g = VGroup(crown, trunk)
    g.move_to([x, y, 0])
    return g


class S05Forest(ProfileScene):
    def construct(self):
        self.add_inset()
        # forest of abstract trees (three staggered rows, back to front)
        rnd = random.Random(11)
        rows = []
        for r, (y, n) in enumerate([(0.55, 10), (-0.15, 10), (-0.85, 10), (-1.55, 10)]):
            row = []
            for i in range(n):
                x = -0.85 + i * 0.68 + (0.36 if r % 2 else 0.0) + rnd.uniform(-0.08, 0.08)
                s = rnd.uniform(1.15, 1.5)
                row.append(tree(x, y + rnd.uniform(-0.06, 0.06), s))
            for t in row:
                t.set_z_index(r)
            rows.append(VGroup(*row))
        # four special trees, picked from the rows
        picks = [rows[0][2], rows[1][5], rows[2][8], rows[3][3]]

        q1 = T("“a primeval forest,", 36, GOLD, font=TITLE_FONT).move_to([PANEL_C, 2.95, 0])
        q2 = T("a monstrous and boundless thicket”", 36, GOLD, font=TITLE_FONT).move_to([PANEL_C, 2.3, 0])
        self.at("What he had opened", lead=0.1)
        door = lab("what he had opened", GREY, 24).move_to([PANEL_C, 0.9, 0])
        self.play(pop(door), run_time=0.5)
        self.at("a primeval forest")
        self.play(ReplacementTransform(door, q1),
                  LaggedStart(*[GrowFromPoint(t, t.get_bottom()) for t in rows[0]], lag_ratio=0.1), run_time=1.5)
        self.at("a monstrous", lead=0.2)
        self.play(FadeIn(q2, shift=UP * 0.1),
                  LaggedStart(*[GrowFromPoint(t, t.get_bottom()) for t in rows[1]], lag_ratio=0.07), run_time=1.1)
        self.at("boundless")
        self.play(LaggedStart(*[GrowFromPoint(t, t.get_bottom()) for t in rows[2]], lag_ratio=0.07), run_time=1.0)

        # Wöhler goes in again
        dot = Dot(radius=0.14, color=GOLD)
        who = T("Wöhler", 24, GOLD).next_to(dot, UP, buff=0.12)
        who.set_stroke(BG, width=8, background=True)
        walker = VGroup(dot, who).move_to([-1.95, -1.1, 0]).set_z_index(10)
        will = T("the willingness to go in again", 26, GOLD).move_to([PANEL_C + 0.4, -3.05, 0]).set_opacity(0)
        self.at("claimed only")
        self.play(FadeIn(walker, shift=UP * 0.1), run_time=0.5)
        self.at("willingness", lead=0.1)
        self.play(will.animate.set_opacity(1.0), run_time=0.5)
        self.at("go in again", lead=0.2)
        self.play(walker.animate.move_to([1.3, -0.7, 0]), run_time=1.1, rate_func=smooth)

        # the four classes
        self.at("The four classes", lead=0.1)
        self.play(FadeOut(will), FadeOut(walker), run_time=0.4)
        four = T("four classes of biomolecules", 28, PINK).move_to([PANEL_C + 0.4, -3.05, 0])
        self.play(pop(four),
                  LaggedStart(*[p.animate.set_color(PINK).set_stroke(opacity=1.0).set_fill(PINK, opacity=0.8).set_z_index(8)
                                for p in picks], lag_ratio=0.3), run_time=1.5)
        self.at("this chapter", lead=0.1)
        self.play(Transform(four, T("four classes of biomolecules in this chapter", 26, PINK).move_to(four)),
                  run_time=0.5)
        self.at("the trees", lead=0.3)
        self.play(*[Indicate(p, color=PINK, scale_factor=1.3) for p in picks], run_time=0.9)
        self.finish()


# ----------------------------------------------------------------------------- s06 the quote
class S06Quote(ProfileScene):
    def construct(self):
        self.add_inset()
        lines = ["“I can no longer, as it were, hold back", "my chemical urine; and I have to let out",
                 "that I can make urea without needing", "a kidney.”"]
        q = VGroup(*[T(l, 36, TEXT, font=TITLE_FONT) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        fit(q, max_w=8.4)
        who = T("— Friedrich Wöhler, in a letter to his mentor Berzelius", 24, GOLD)
        g = VGroup(q, who).arrange(DOWN, aligned_edge=RIGHT, buff=0.5).move_to([PANEL_C, 0.1, 0])
        for ln in q:
            ln.set_opacity(0)
        who.set_opacity(0)
        self.add(g)
        self.wait(0.3)
        for ln in q:
            self.play(ln.animate.set_opacity(1.0), run_time=0.7)
        self.wait(0.4)
        self.play(who.animate.set_opacity(1.0), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s07 end card
class S07End(EndCard):
    LINE = "Made urea from inorganic salt in 1828, ending the living/dead chemistry divide."

    def construct(self):
        img, frame = portrait_pair(2.3)
        grp = Group(img, frame).move_to([0, 2.0, 0])
        cap = T(CAPTION, 22, GREY, font=TITLE_FONT).next_to(frame, DOWN, buff=0.18)
        a = T("Made urea from inorganic salt in 1828,", size=40, font=TITLE_FONT)
        b = T("ending the living/dead chemistry divide.", size=40, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.22).move_to([0, -0.7, 0])
        sub = T("biochemistrypedia.com", size=24, color=TEAL).move_to([0, -2.1, 0])
        src = T("Source: The Molecule Hunters (v10) · Wöhler profile", 22, GREY).move_to([0, -2.8, 0])
        self.play(FadeIn(img), FadeIn(frame), FadeIn(cap), run_time=0.5)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(sub), FadeIn(src), run_time=0.4)
        self.finish()
