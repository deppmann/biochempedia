"""Linus Pauling: a scientist profile (Biochemistrypedia, water-weak-bonds lesson).

Narration is the lesson entry's `story`, verbatim. Everything on screen comes from that entry
(name, dates, contribution, story, quote). The portrait is an AI-generated engraving-style
illustration from The Molecule Hunters; it is captioned "illustration · AI-generated" whenever it is
on screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = time and naming: Pauling's name/dates, "only later", "late in the night"
  TEAL   = Pauling's chemistry: the chain of residue tiles, the helix and its numbers, "the geometry"
  YELLOW = tools and data: the sheet of paper, the experiment
  RED    = what stood in the way: the sinus infection, forcing the chain closed
  GREEN  = hydrogen bonds (carbonyl CO to amide NH)
  GREY   = axes, brackets, de-emphasized things (no lab, no model kit, the assumption)
No molecular structure is drawn: the chain is a row of residue tiles; the helix is the same tiles
placed on a helical track (side view, front tiles bright, back tiles dim); the rise is a bracket.
"""
import math

import numpy as np
from bp_style import *  # noqa: F401,F403

PORTRAIT = "/Users/deppmann/biochempedia/public/scientists/linus-pauling.png"
CAPTION = "illustration · AI-generated"

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
    def add_inset(self):
        img, frame, cap, tag, rule = inset_group()
        self.add(img, frame, cap, tag, rule)


def plain_tile(color=TEAL, size=0.6):
    return RoundedRectangle(corner_radius=0.09, width=size, height=size, stroke_color=color, stroke_width=3,
                            fill_color=ManimColor(BG).interpolate(ManimColor(color), 0.2), fill_opacity=1)


def num_tile(n, dim=0.0, size=0.5, fs=24):
    """Numbered residue tile; dim in [0,1] fades colours toward the background (opaque, so it can sit 'behind')."""
    col = interpolate_color(ManimColor(TEAL), ManimColor(BG), dim)
    sq = RoundedRectangle(corner_radius=0.08, width=size, height=size, stroke_color=col, stroke_width=3,
                          fill_color=ManimColor(BG).interpolate(ManimColor(col), 0.2), fill_opacity=1)
    return VGroup(sq, M(str(n), fs, col).move_to(sq))


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


# ----------------------------------------------------------------------------- s01 flat on his back
class S01Found(ProfileScene):
    def construct(self):
        self.add_inset()
        top = lab("the most important fold in biology", TEAL, 30).move_to([PANEL_C, 2.7, 0])
        self.at("important fold in biology", lead=0.7)
        self.play(pop(top), run_time=0.6)

        back = lab("flat on his back", TEXT, 30).move_to([-0.1, 1.2, 0])
        self.at("flat on his back")
        self.play(pop(back), run_time=0.45)
        sinus = lab("sinus infection", RED, 30).move_to([3.9, 1.2, 0])
        self.at("sinus infection")
        self.play(pop(sinus), run_time=0.45)
        paper = lab("a sheet of paper", YELLOW, 30).move_to([PANEL_C, -0.1, 0])
        self.at("sheet of paper")
        self.play(pop(paper), run_time=0.45)

        # second sentence: what he did NOT have, and the assumption he refused
        self.at("No lab", lead=0.45)
        self.play(FadeOut(VGroup(top, back, sinus, paper)), run_time=0.4)
        nolab = lab("no lab", GREY, 30).move_to([0.3, 2.5, 0])
        nokit = lab("no model kit", GREY, 30).move_to([3.7, 2.5, 0])
        self.at("No lab")
        self.play(pop(nolab), run_time=0.4)
        self.at("model kit")
        self.play(pop(nokit), run_time=0.4)

        n, dx, x0, y = 6, 0.85, -0.45, 0.0
        tiles = [plain_tile().move_to([x0 + dx * i, y, 0]).set_z_index(3) for i in range(n)]
        links = [Line(tiles[i].get_center(), tiles[i + 1].get_center(), color=TEAL, stroke_width=4).set_z_index(1)
                 for i in range(n - 1)]
        chain_lab = T("a chain", 32, TEAL).move_to([PANEL_C - 0.2, y + 0.95, 0])
        self.at("just a chain")
        self.add(*links)
        self.play(FadeIn(chain_lab, shift=UP * 0.1),
                  LaggedStart(*[FadeIn(t, shift=UP * 0.12) for t in tiles], lag_ratio=0.2), run_time=1.0)

        # forcing the chain closed: an arch from the last tile back to the first, then crossed out
        first, last = tiles[0].get_top() + UP * 0.05, tiles[-1].get_top() + UP * 0.05
        arch = CurvedArrow(last, first, angle=PI * 0.62, color=RED, stroke_width=5, tip_length=0.22).set_z_index(2)
        self.at("refused to force closed", lead=0.2)
        self.play(FadeOut(chain_lab), Create(arch), run_time=0.7)
        mid = arch.point_from_proportion(0.5)
        cross = VGroup(Line([-0.28, -0.28, 0], [0.28, 0.28, 0]), Line([-0.28, 0.28, 0], [0.28, -0.28, 0])) \
            .set_color(RED).set_stroke(width=9).move_to(mid).set_z_index(5)
        self.play(FadeIn(cross, scale=1.5), run_time=0.3)

        # "after a whole number of residues": a bracket under the chain
        by = y - 0.75
        br = VGroup(Line([x0 - 0.3, by, 0], [x0 + dx * (n - 1) + 0.3, by, 0]),
                    Line([x0 - 0.3, by, 0], [x0 - 0.3, by + 0.18, 0]),
                    Line([x0 + dx * (n - 1) + 0.3, by, 0], [x0 + dx * (n - 1) + 0.3, by + 0.18, 0])) \
            .set_color(GREY).set_stroke(width=4)
        whole = lab("a whole number of residues", GREY, 28).move_to([x0 + dx * (n - 1) / 2, by - 0.75, 0])
        self.at("whole number of residues", lead=0.4)
        self.play(Create(br), pop(whole), run_time=0.7)

        # "the way everyone else had assumed it must"
        assume = T("the way everyone else assumed it must", 28, GREY).move_to([PANEL_C - 0.2, -2.9, 0])
        self.at("everyone else", lead=0.3)
        self.play(FadeIn(assume, shift=UP * 0.1), run_time=0.6)
        self.finish()


# ----------------------------------------------------------------------------- s02 folding the paper
class S02Fold(ProfileScene):
    def construct(self):
        self.add_inset()
        sx, sy, w, h = PANEL_C, 2.0, 6.6, 1.2
        paper = Rectangle(width=w, height=h, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW,
                          fill_opacity=0.12).move_to([sx, sy, 0])
        paper_lab = T("paper", 30, YELLOW).next_to(paper, UP, buff=0.18, aligned_edge=LEFT)
        creases = VGroup(*[DashedLine([cx - 0.28 * s, sy + h / 2, 0], [cx + 0.28 * s, sy - h / 2, 0], color=YELLOW,
                                      stroke_width=3, dash_length=0.1)
                           for cx, s in [(sx - 2.2, 1), (sx, -1), (sx + 2.2, 1)]])
        self.add(paper_lab)
        self.play(Create(paper), Create(creases), run_time=0.6)

        ang = lab("roughly the right bond angles", TEAL, 30).move_to([sx, 0.15, 0])
        link1 = Arrow(ang.get_top(), [sx, sy - h / 2 - 0.05, 0], color=TEAL, stroke_width=4, buff=0.08,
                      max_tip_length_to_length_ratio=0.3)
        self.at("roughly the right bond angles", lead=0.3)
        self.play(pop(ang), GrowArrow(link1), run_time=0.6)

        geo = lab("the geometry decides", TEAL, 40, pad=0.3, fill=0.22).move_to([sx, -1.9, 0])
        link2 = Arrow(ang.get_bottom(), geo.get_top(), color=TEAL, stroke_width=4, buff=0.08,
                      max_tip_length_to_length_ratio=0.3)
        self.at("he let the geometry decide", lead=0.2)
        self.play(GrowArrow(link2), pop(geo), run_time=0.6)
        self.play(Indicate(geo, color=TEAL, scale_factor=1.05), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- s03 the helix
class S03Helix(ProfileScene):
    CX = 4.3             # helix axis x
    R = 1.1              # helix radius in the picture
    DY = 0.58            # rise per residue (3.6 residues = one turn)
    Y1 = -2.45           # y of residue 1
    PHI = -20.0          # angle of residue 1 (deg); 100 deg per residue = 3.6 per turn

    def theta(self, n):
        return math.radians(self.PHI + 100.0 * (n - 1))

    def pos(self, n):
        th = self.theta(n)
        return np.array([self.CX + self.R * math.cos(th), self.Y1 + self.DY * (n - 1), 0.0])

    def depth(self, n):          # 0 = nearest the viewer, else behind (sin<0 is the near side)
        return 0.0 if math.sin(self.theta(n)) < -0.05 else 0.4

    def track(self):
        """The helix itself, as the real side-view curve x = R cos(t), y = rise * t:
        near half-turns bright and in front, far half-turns dim and behind."""
        lo, hi = self.PHI, self.PHI + 100.0 * 8
        out = []
        a = math.floor(lo / 180.0) * 180.0
        while a < hi:
            t0, t1 = max(a, lo), min(a + 180.0, hi)
            front = (a % 360.0) == 180.0
            f = lambda t: np.array([self.CX + self.R * math.cos(math.radians(t)),
                                    self.Y1 + self.DY * (t - self.PHI) / 100.0, 0.0])
            col = TEAL if front else interpolate_color(ManimColor(TEAL), ManimColor(BG), 0.35)
            seg = ParametricFunction(f, t_range=[t0, t1, 3.0], color=col, stroke_width=6 if front else 4)
            seg.set_z_index(2.6 if front else 1)
            out.append(seg)
            a += 180.0
        return out

    def construct(self):
        self.add_inset()
        N = 9
        axis = DashedLine([self.CX, -3.0, 0], [self.CX, 2.95, 0], color=GREY, stroke_width=2.5, dash_length=0.12)
        axis.set_z_index(0)
        tiles = []
        for n in range(1, N + 1):
            t = num_tile(n, dim=self.depth(n), size=0.52, fs=24).move_to(self.pos(n))
            t.set_z_index(3 if self.depth(n) == 0 else 2)
            tiles.append(t)
        curves = self.track()
        helix = VGroup(*curves, *tiles)

        untidy = lab("untidy on purpose", TEAL, 30).move_to([0.15, 2.5, 0])
        self.at("untidy on", lead=0.2)
        self.play(pop(untidy), run_time=0.5)

        rh = lab(["right-handed", "helix"], TEAL, 30).move_to([0.15, 1.2, 0])
        self.at("right handed helix", lead=0.3)
        self.play(pop(rh), FadeIn(axis), LaggedStart(*[Create(c) for c in curves], lag_ratio=0.25),
                  LaggedStart(*[FadeIn(t, scale=0.7) for t in tiles], lag_ratio=0.2), run_time=1.8)

        # one turn = 3.6 residues = 5.4 angstroms: a bracket on the left of the helix, between two guides
        yb, yt = self.Y1, self.Y1 + 3.6 * self.DY
        bx = 2.35
        gx = self.CX - self.R - 0.4
        g1 = DashedLine([bx, yb, 0], [gx, yb, 0], color=GREY, stroke_width=2.5, dash_length=0.1)
        g2 = DashedLine([bx, yt, 0], [gx, yt, 0], color=GREY, stroke_width=2.5, dash_length=0.1)
        turn = DoubleArrow([bx, yb, 0], [bx, yt, 0], color=TEAL, stroke_width=5, buff=0, tip_length=0.2)
        per_turn = lab(["every 3.6 residues"], TEAL, 28).move_to([0.0, -0.6, 0])
        self.at("every 3 6 residues", lead=0.3)
        self.play(Create(g1), Create(g2), GrowFromCenter(turn), run_time=0.7)
        self.play(pop(per_turn), run_time=0.45)
        rise = lab(["rising 5.4 Å", "per turn"], TEAL, 28).move_to([0.0, -1.8, 0])
        self.at("5 4 angstroms", lead=0.3)
        self.play(pop(rise), run_time=0.5)
        self.at("per turn", lead=-0.2)
        self.play(Indicate(turn, color=TEAL, scale_factor=1.08), run_time=0.6)

        # hydrogen bonds: clear the left side, then CO of residue 1 reaches up to NH of residue 5
        self.at("with each carbonyl", lead=0.3)
        self.play(FadeOut(VGroup(untidy, rh, per_turn, rise, g1, g2, turn)), run_time=0.4)
        co = lab("carbonyl oxygen (CO)", GREEN, 26).move_to([0.15, self.Y1, 0])
        co_line = Line(co.get_right() + RIGHT * 0.05, self.pos(1) + LEFT * 0.3, color=GREEN, stroke_width=3)
        self.at("carbonyl oxygen", lead=0.3)
        self.play(pop(co), Create(co_line), Indicate(tiles[0], color=GREEN, scale_factor=1.15), run_time=0.6)

        bond = lambda a, b: Arrow(self.pos(a) + UP * 0.3, self.pos(b) + DOWN * 0.3, color=GREEN, stroke_width=5,
                                  buff=0, max_tip_length_to_length_ratio=0.3).set_z_index(5)
        first = bond(1, 5)
        self.at("reaching up the axis", lead=0.1)
        self.play(GrowArrow(first), run_time=1.2)
        nh = lab("amide hydrogen (NH)", GREEN, 26).move_to([0.15, self.pos(5)[1], 0])
        nh_line = Line(nh.get_right() + RIGHT * 0.05, self.pos(5) + LEFT * 0.3, color=GREEN, stroke_width=3)
        self.at("amide hydrogen", lead=0.3)
        self.play(pop(nh), Create(nh_line), Indicate(tiles[4], color=GREEN, scale_factor=1.15), run_time=0.6)

        # four residues along: count them
        four = lab("four residues along", GREEN, 26).move_to([0.15, self.Y1 + 2 * self.DY, 0])
        self.at("four residues", lead=0.3)
        self.play(pop(four), run_time=0.4)
        self.play(LaggedStart(*[Indicate(tiles[i], color=GREEN, scale_factor=1.18) for i in (1, 2, 3, 4)],
                              lag_ratio=0.5), run_time=1.6)

        # a regular ladder: every CO reaches four along (helix dimmed so the bonds read)
        ladder_lab = lab(["a regular ladder of", "hydrogen bonds"], GREEN, 26).move_to([0.15, 1.1, 0])
        self.at("regular ladder", lead=0.3)
        self.play(pop(ladder_lab), helix.animate.set_opacity(0.35), FadeOut(co_line), FadeOut(nh_line), run_time=0.4)
        rest = [bond(n, n + 4) for n in range(2, 6)]
        self.play(LaggedStart(*[GrowArrow(b) for b in rest], lag_ratio=0.4), run_time=1.5)

        # parallel to the helix axis
        par = lab(["running parallel to", "the helix axis"], TEXT, 26).move_to([0.15, 2.65, 0])
        axis_arrow = Arrow([self.CX, -3.0, 0], [self.CX, 3.0, 0], color=TEXT, stroke_width=4, buff=0,
                           max_tip_length_to_length_ratio=0.05).set_z_index(0)
        self.at("parallel to the helix axis", lead=0.3)
        self.play(pop(par), FadeOut(axis), Create(axis_arrow), run_time=0.6)
        self.play(Indicate(axis_arrow, color=TEXT, scale_factor=1.0), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- s04 reading the structure off the bonds
class S04Name(ProfileScene):
    def construct(self):
        self.add_inset()
        bonding = lab("the bonding", GREEN, 32).move_to([-0.4, 1.7, 0])
        structure = lab("the structure", TEAL, 32).move_to([4.2, 1.7, 0])
        arrow = Arrow(bonding.get_right() + RIGHT * 0.1, structure.get_left() + LEFT * 0.1, color=TEXT, stroke_width=4,
                      buff=0, max_tip_length_to_length_ratio=0.25)
        read = T("read", 28, TEXT).next_to(arrow, UP, buff=0.12)
        self.at("read the structure", lead=0.2)
        self.play(pop(structure), run_time=0.45)
        self.at("off the bonding", lead=0.1)
        self.play(pop(bonding), GrowArrow(arrow), FadeIn(read), run_time=0.6)
        everything = T("the way he read everything", 30, GREY).move_to([PANEL_C, 0.35, 0])
        self.at("the way he read everything", lead=0.2)
        self.play(FadeIn(everything, shift=UP * 0.1), run_time=0.5)

        # naming it
        alpha = lab("alpha helix", TEAL, 46, pad=0.32, fill=0.22).move_to([PANEL_C, 0.8, 0])
        self.at("He called it", lead=0.5)
        self.play(FadeOut(VGroup(bonding, arrow, read, everything)),
                  FadeTransform(structure, alpha), run_time=0.7)
        self.at("the alpha helix", lead=0.1)
        self.play(Indicate(alpha, color=TEAL, scale_factor=1.07), run_time=0.8)

        # could not let it go: a dot that keeps circling it
        ew, eh = alpha.width + 1.7, alpha.height + 1.5
        orbit = Ellipse(width=ew, height=eh, color=GOLD, stroke_width=3).set_stroke(opacity=0.35).move_to(alpha)
        dot = Dot(radius=0.13, color=GOLD)
        ph = ValueTracker(0.0)
        rate = [0.8]
        c = alpha.get_center()
        dot.add_updater(lambda m, dt: (ph.increment_value(dt * rate[0]),
                                       m.move_to(c + np.array([ew / 2 * math.cos(ph.get_value()),
                                                               eh / 2 * math.sin(ph.get_value()), 0]))))
        dot.move_to(c + np.array([ew / 2, 0, 0]))
        self.at("could not let it go", lead=0.2)
        self.play(Create(orbit), FadeIn(dot), run_time=0.5)
        self.add(dot)

        # the quote, in four beats: pleased, stayed up, late in the night, pondering
        pleased = T("so pleased with this structure", 30, TEAL).move_to([PANEL_C, 2.8, 0])
        self.at("so pleased with this structure", lead=0.3)
        self.play(FadeIn(pleased, shift=UP * 0.1), Indicate(alpha, color=TEAL, scale_factor=1.08), run_time=0.6)
        late = lab(["stayed up until", "late in the night"], GOLD, 30).move_to([PANEL_C, -1.5, 0])
        self.at("I stayed up", lead=0.3)
        self.play(pop(late), run_time=0.5)
        self.at("pondering", lead=0.3)
        rate[0] = 1.6
        self.play(Indicate(alpha, color=GOLD, scale_factor=1.1), run_time=0.9)
        self.finish()


# ----------------------------------------------------------------------------- s05 experiment confirmed it only later
class S05Later(ProfileScene):
    def construct(self):
        self.add_inset()
        ay = 0.9
        axis = Arrow([-2.0, ay, 0], [6.1, ay, 0], color=GREY, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.04)
        helix = lab("alpha helix", TEAL, 30).move_to([-0.1, ay + 1.15, 0])
        d1 = Dot([-0.1, ay, 0], radius=0.12, color=TEAL)
        self.add(axis, d1, helix)      # carried over from the previous scene: the named helix
        exper = lab("experiment", YELLOW, 30).move_to([4.2, ay + 1.15, 0])
        d2 = Dot([4.2, ay, 0], radius=0.12, color=YELLOW)
        self.at("Experiment", lead=0.1)
        self.play(FadeIn(d2, scale=2), pop(exper), run_time=0.45)
        check = VGroup(Line([-0.22, 0.0, 0], [-0.06, -0.2, 0]), Line([-0.06, -0.2, 0], [0.28, 0.24, 0])) \
            .set_color(YELLOW).set_stroke(width=8).next_to(exper, RIGHT, buff=0.15)
        self.at("confirmed", lead=0.1)
        self.play(Create(check), run_time=0.35)
        later = T("only later", 30, GOLD, weight=BOLD).move_to([2.05, ay - 0.5, 0])
        self.at("only later", lead=0.1)
        self.play(FadeIn(later, shift=UP * 0.1), run_time=0.4)
        geo = lab("the geometry had been enough", TEAL, 36, pad=0.3, fill=0.22).move_to([PANEL_C, -1.7, 0])
        self.at("the geometry had been enough", lead=0.2)
        self.play(pop(geo), run_time=0.5)
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
    LINE = "Derived the alpha helix from hydrogen-bond geometry alone; gave chemistry bonding vocabulary."

    def construct(self):
        a = T("Derived the alpha helix from", size=42, font=TITLE_FONT)
        b = T("hydrogen-bond geometry alone;", size=42, font=TITLE_FONT)
        c = T("gave chemistry bonding vocabulary.", size=42, font=TITLE_FONT)
        line = VGroup(a, b, c).arrange(DOWN, buff=0.22)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
