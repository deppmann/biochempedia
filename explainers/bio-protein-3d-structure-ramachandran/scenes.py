"""G. N. Ramachandran: a scientist profile (Biochemistrypedia, protein-3d-structure lesson).

Narration is the lesson entry's `story`, verbatim. Everything on screen comes from that entry
(name, dates, contribution, story). The entry has no quotes, so there is no quote scene.
The portrait is an AI-generated engraving-style illustration from The Molecule Hunters; it is
captioned "illustration · AI-generated" whenever it is on screen at a readable size.

COLOR MAP (one color per concept, whole video)
  GOLD   = time and recognition: name/dates, 1963, sixty years on, 2001, the prizes, the 53 years
  TEAL   = his science: physics, the angles phi/psi, the plot, the allowed combinations and islands
  YELLOW = people and the structures being checked: C. V. Raman, the two colleagues, new structures
  RED    = what is ruled out or lost: atoms colliding, forbidden combinations, never called, Parkinson's, loss
  PLACE (lavender) = places and institutions: University of Madras, Nobel Committee, Chennai
  GREEN  = the sanity check passing
  GREY   = axes, grids, "almost nothing", de-emphasized things
No molecular structure is drawn: the chain is a row of plain residue tiles, the plot is a schematic
grid of cells (labelled "schematic"): which cells are shaded is illustrative, not data.
"""
import os
from pathlib import Path

import numpy as np
from bp_style import *  # noqa: F401,F403

NAME = "G. N. Ramachandran"
DATES = "1922–2001"
CAPTION = "illustration · AI-generated"
PLACE = "#B39DDB"       # places and institutions
IMG = str(Path(os.environ.get("KX_SCRIPT", __file__)).resolve().parent / "ramachandran_crop.png")
CROP_AR = 520 / 685.0

# left column (portrait inset + name), right panel (the story animates here)
INSET_C = np.array([-4.75, 1.3, 0.0])
INSET_H = 3.5
PANEL_C = 1.95          # x center of the right panel (x from -2.4 to 6.3)


# ----------------------------------------------------------------------------- helpers
def portrait_pair(height):
    img = ImageMobject(IMG).set_height(height)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["cubic"])
    frame = Rectangle(width=img.width, height=img.height, stroke_color=GOLD, stroke_width=3, fill_opacity=0)
    return img, frame


def caption_under(frame, size=22):
    return T(CAPTION, size=size, color=GREY, font=TITLE_FONT).next_to(frame, DOWN, buff=0.2)


def name_tag(frame):
    nm = T(NAME, size=27, font=TITLE_FONT)
    dt = T(DATES, size=28, color=GOLD)
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


def cross(center, s=0.22, color=RED, w=8):
    return VGroup(Line([-s, -s, 0], [s, s, 0]), Line([-s, s, 0], [s, -s, 0])) \
        .set_color(color).set_stroke(width=w).move_to(center)


def check(center, s=0.24, color=GREEN, w=8):
    return VGroup(Line([-s, 0.0, 0], [-s * 0.3, -s * 0.8, 0]), Line([-s * 0.3, -s * 0.8, 0], [s, s * 0.9, 0])) \
        .set_color(color).set_stroke(width=w).move_to(center)


class ProfileScene(SpokenScene):
    """SpokenScene that starts with the inset (portrait + name) already on screen."""

    def add_inset(self):
        img, frame, cap, tag, rule = inset_group()
        self.add(img, frame, cap, tag, rule)


# ---- the schematic phi-psi plane -------------------------------------------------------
N = 24
ISLANDS = {   # (u, v) centre and radii in plot units where the plane spans -1..1 (illustrative shapes)
    "alpha": (-0.35, -0.25, 0.21, 0.21),
    "beta": (-0.65, 0.70, 0.29, 0.23),
}


def allowed(u, v):
    for cu, cv, ru, rv in ISLANDS.values():
        if ((u - cu) / ru) ** 2 + ((v - cv) / rv) ** 2 <= 1.0:
            return True
    return False


def make_plane(center, half):
    """Return (frame, forbidden cells, allowed cells, geometry fn). Cells are plain squares."""
    cs = 2 * half / N
    forb, allow = VGroup(), VGroup()
    for i in range(N):
        for j in range(N):
            u = -1 + (i + 0.5) * 2 / N
            v = -1 + (j + 0.5) * 2 / N
            sq = Square(side_length=cs, stroke_width=0.6, stroke_color=GREY, stroke_opacity=0.45, fill_opacity=0)
            sq.move_to([center[0] - half + (i + 0.5) * cs, center[1] - half + (j + 0.5) * cs, 0])
            (allow if allowed(u, v) else forb).add(sq)
    frame = Square(side_length=2 * half, stroke_color=GREY, stroke_width=2.5, fill_opacity=0).move_to(
        [center[0], center[1], 0])

    def pos(u, v):
        return np.array([center[0] + u * half, center[1] + v * half, 0.0])

    return frame, forb, allow, pos


def island_outline(pos, half, key, color=TEAL):
    cu, cv, ru, rv = ISLANDS[key]
    e = Ellipse(width=2 * ru * half * 1.12, height=2 * rv * half * 1.12, stroke_color=color, stroke_width=4,
                fill_opacity=0)
    return e.move_to(pos(cu, cv))


def tile(color=TEAL, size=0.6):
    return RoundedRectangle(corner_radius=0.09, width=size, height=size, stroke_color=color, stroke_width=3,
                            fill_color=ManimColor(BG).interpolate(ManimColor(color), 0.2), fill_opacity=1)


# ----------------------------------------------------------------------------- s00 title
class S00Title(TitleCard):
    LESSON = "Scientist profile"
    TITLE = NAME

    def construct(self):
        img, frame = portrait_pair(4.7)
        grp = Group(img, frame)
        grp.move_to([-3.4, 0.35, 0])
        cap = caption_under(frame, size=24).shift(DOWN * 0.15)
        brand = T("BIOCHEMISTRYPEDIA", size=20, color=TEAL, weight=BOLD).set_opacity(0.9)
        lesson = T(self.LESSON.upper(), size=22, color=GREY)
        name = T(self.TITLE, size=54, font=TITLE_FONT)
        fit(name, max_w=6.6)
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


# ----------------------------------------------------------------------------- s01 Madras
class S01Madras(ProfileScene):
    def construct(self):
        self.add_inset()
        phys = lab("physicist", TEAL, 32).move_to([-0.5, 2.1, 0])
        self.at("physicist")
        self.play(pop(phys), run_time=0.5)

        raman = lab("C. V. Raman", YELLOW, 32).move_to([4.0, 2.1, 0])
        arrow = Arrow(phys.get_right() + RIGHT * 0.15, raman.get_left() + LEFT * 0.15, color=GREY, stroke_width=4,
                      buff=0, max_tip_length_to_length_ratio=0.25)
        under = T("under", 26, GREY).next_to(arrow, UP, buff=0.12)
        self.at("under")
        self.play(GrowArrow(arrow), FadeIn(under), run_time=0.4)
        self.at("C. V.")
        self.play(pop(raman), run_time=0.5)

        # Madras as a place; the department is built inside it, out of almost nothing
        region = RoundedRectangle(corner_radius=0.2, width=8.3, height=3.0, stroke_color=PLACE, stroke_width=2.5,
                                  fill_color=PLACE, fill_opacity=0.08).move_to([PANEL_C, -1.15, 0])
        region_lab = T("University of Madras", 30, PLACE).move_to(region.get_top() + DOWN * 0.5 + LEFT * 2.1)
        dept = lab(["new physics", "department"], TEAL, 30).move_to([4.0, -1.75, 0])
        self.at("built")
        self.play(GrowFromCenter(dept), run_time=0.6)
        self.at("University of Madras")
        self.play(FadeIn(region), FadeIn(region_lab, shift=UP * 0.1), run_time=0.6)
        nothing = lab(["almost", "nothing"], GREY, 30, fill=0.05).move_to([-0.2, -1.75, 0])
        nothing[1].set_color("#B8BEC8")
        build = Arrow(nothing.get_right() + RIGHT * 0.15, dept.get_left() + LEFT * 0.15, color=TEAL, stroke_width=5,
                      buff=0, max_tip_length_to_length_ratio=0.25)
        self.at("from almost nothing")
        self.play(pop(nothing), run_time=0.5)
        self.play(GrowArrow(build), Indicate(dept, color=TEAL, scale_factor=1.08), run_time=0.7)
        self.finish()


# ----------------------------------------------------------------------------- s02 the question
class S02Question(ProfileScene):
    def construct(self):
        self.add_inset()
        ay = 2.45
        axis = Arrow([-2.2, ay, 0], [6.1, ay, 0], color=GREY, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.04)
        dot = Dot([-1.2, ay, 0], radius=0.12, color=GOLD)
        date = T("1963", 38, GOLD, weight=BOLD).next_to(dot, UP, buff=0.2).shift(RIGHT * 0.45)
        self.at("1963")
        self.play(Create(axis), FadeIn(dot, scale=2), FadeIn(date, shift=UP * 0.1), run_time=0.6)

        me = lab("Ramachandran", GOLD, 28)
        c1 = lab("colleague", YELLOW, 28)
        c2 = lab("colleague", YELLOW, 28)
        VGroup(me, c1, c2).arrange(RIGHT, buff=0.4).move_to([PANEL_C, 1.1, 0])
        self.play(pop(me), run_time=0.4)
        self.at("two colleagues")
        self.play(pop(c1), run_time=0.4)
        self.play(pop(c2), run_time=0.4)

        q = lab(["a question no one had", "put precisely before"], GOLD, 32).move_to([PANEL_C, -0.5, 0])
        qmark = T("?", 80, GOLD, weight=BOLD).next_to(q, RIGHT, buff=0.3)
        people = VGroup(me, c1, c2)
        down = Arrow([PANEL_C, 0.55, 0], [PANEL_C, 0.2, 0], color=GREY, stroke_width=4, buff=0,
                     max_tip_length_to_length_ratio=0.5)
        self.at("asked a question")
        self.play(pop(q), run_time=0.5)
        self.at("no one had put")
        self.play(FadeIn(qmark, scale=1.5), run_time=0.5)
        self.play(Indicate(q, color=GOLD, scale_factor=1.05), run_time=0.7)

        # the question itself: a chain of amino acids, a pair of angles, a ban on collisions
        self.at("For every amino", lead=0.9)
        self.play(FadeOut(VGroup(people, q, qmark)), run_time=0.5)
        tiles = VGroup(*[tile() for _ in range(7)]).arrange(RIGHT, buff=0.55).move_to([PANEL_C, 0.7, 0])
        links = VGroup(*[Line(tiles[i].get_right(), tiles[i + 1].get_left(), color=TEAL, stroke_width=5)
                         for i in range(6)])
        every = lab("every amino acid", TEAL, 28).move_to([PANEL_C - 1.9, 2.0 - 0.02, 0]).shift(UP * 0.0)
        every.next_to(tiles, UP, buff=0.35).align_to(tiles, LEFT)
        self.at("every amino")
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.08), FadeIn(links),
                  run_time=0.8)
        self.play(pop(every), LaggedStart(*[Indicate(t, color=TEAL, scale_factor=1.15) for t in tiles],
                                          lag_ratio=0.07), run_time=0.7)
        chain_lab = T("in a chain", 28, GREY).next_to(tiles, DOWN, buff=0.25).align_to(tiles, RIGHT)
        self.at("in a chain")
        self.play(FadeIn(chain_lab, shift=UP * 0.1), run_time=0.4)

        pairs = lab("pairs of backbone angles", TEAL, 30).move_to([PANEL_C, -0.95, 0])
        self.at("which pairs of")
        self.play(pop(pairs), run_time=0.5)
        phi = lab("φ  (phi)", TEAL, 34).move_to([0.3, -1.95, 0])
        psi = lab("ψ  (psi)", TEAL, 34).move_to([3.6, -1.95, 0])
        self.at("phi")
        self.play(pop(phi), run_time=0.45)
        self.at("psi")
        self.play(pop(psi), run_time=0.45)

        ok = lab("possible", GREEN, 28).move_to([-0.7, -2.95, 0])
        wo = T("without", 28, GREY).move_to([1.05, -2.95, 0])
        bad = lab("atoms colliding", RED, 28).move_to([3.6, -2.95, 0])
        self.at("possible without")
        self.play(pop(ok), FadeIn(wo), run_time=0.5)
        self.at("atoms colliding")
        self.play(pop(bad), run_time=0.45)
        self.play(FadeIn(cross(bad.get_right() + RIGHT * 0.45, 0.22), scale=1.4), run_time=0.4)
        self.finish()


# ----------------------------------------------------------------------------- s03 the plot
class S03Plot(ProfileScene):
    CENTER = np.array([2.9, 0.25, 0.0])
    HALF = 2.16

    def construct(self):
        self.add_inset()
        frame, forb, allow, pos = make_plane(self.CENTER, self.HALF)
        cells = VGroup(*forb, *allow)
        order = list(range(len(cells)))
        rng = np.random.default_rng(7)
        rng.shuffle(order)

        calc = lab(["allowed", "distances"], TEAL, 28).move_to([-1.2, 1.7, 0])
        self.at("They calculated")
        self.play(FadeIn(frame), pop(calc), run_time=0.5)
        self.at("allowed distances")
        # every cell is tested in turn: a sweep of the whole plane
        self.play(LaggedStart(*[FadeIn(cells[i]) for i in order], lag_ratio=0.004), run_time=1.5)

        # forbidden combinations are shaded
        forb_lab = lab("forbidden", RED, 28).move_to([-1.2, -0.5, 0])
        self.at("shaded the forbidden")
        fo = list(range(len(forb)))
        rng.shuffle(fo)
        self.play(LaggedStart(*[forb[i].animate.set_fill(RED, opacity=0.4).set_stroke(RED, opacity=0.5, width=0.6)
                                for i in fo], lag_ratio=0.01), run_time=1.9)
        self.play(pop(forb_lab), run_time=0.4)

        # axes, one at a time
        phi_ax = Arrow(pos(-1, -1) + DOWN * 0.1 + LEFT * 0.1, pos(1, -1) + DOWN * 0.1 + RIGHT * 0.2, color=TEXT,
                       stroke_width=4, buff=0, max_tip_length_to_length_ratio=0.04)
        psi_ax = Arrow(pos(-1, -1) + DOWN * 0.1 + LEFT * 0.1, pos(-1, 1) + UP * 0.2 + LEFT * 0.1, color=TEXT,
                       stroke_width=4, buff=0, max_tip_length_to_length_ratio=0.04)
        phi_t = T("φ", 40, TEXT).move_to(pos(0, -1) + DOWN * 0.55)
        psi_t = T("ψ", 40, TEXT).move_to(pos(-1, 0.22) + LEFT * 0.5)
        self.at("plotted the result")
        self.play(FadeOut(calc), FadeOut(forb_lab), run_time=0.4)
        self.at("axis")
        self.play(Create(phi_ax), FadeIn(phi_t, shift=UP * 0.1), run_time=0.5)
        self.at("axis", nth=1)
        self.play(Create(psi_ax), FadeIn(psi_t, shift=RIGHT * 0.1), run_time=0.5)
        schem = T("schematic", 24, GREY, font=TITLE_FONT).move_to(pos(1, -1) + DOWN * 0.55 + LEFT * 0.2)
        self.play(FadeIn(schem), run_time=0.3)

        # survivors: the allowed cells light up, then outlines mark two islands
        self.at("survivors clustered")
        self.play(LaggedStart(*[a.animate.set_fill(TEAL, opacity=0.6).set_stroke(TEAL, opacity=0.9, width=1.2)
                                for a in allow], lag_ratio=0.05), run_time=1.3)
        isl_a = island_outline(pos, self.HALF, "alpha")
        isl_b = island_outline(pos, self.HALF, "beta")
        self.at("two compact islands")
        self.play(Create(isl_b), run_time=0.6)
        self.play(Create(isl_a), run_time=0.6)

        lab_a = lab("alpha helix", TEAL, 28).move_to([-1.15, pos(*ISLANDS["alpha"][:2])[1], 0])
        lab_b = lab("beta sheet", TEAL, 28).move_to([-1.15, pos(*ISLANDS["beta"][:2])[1], 0])
        lead_a = Arrow(lab_a.get_right() + RIGHT * 0.1, isl_a.get_left() + LEFT * 0.05, color=TEAL, stroke_width=4,
                       buff=0, max_tip_length_to_length_ratio=0.15)
        lead_b = Arrow(lab_b.get_right() + RIGHT * 0.1, isl_b.get_left() + LEFT * 0.05, color=TEAL, stroke_width=4,
                       buff=0, max_tip_length_to_length_ratio=0.2)
        self.at("alpha helix")
        self.play(pop(lab_a), GrowArrow(lead_a), Indicate(isl_a, color=TEXT, scale_factor=1.15), run_time=0.7)
        self.at("beta sheet")
        self.play(pop(lab_b), GrowArrow(lead_b), Indicate(isl_b, color=TEXT, scale_factor=1.12), run_time=0.7)

        # the rest of the plane: nearly empty
        empty = lab("nearly empty", RED, 28, fill=0.0).move_to(pos(0.45, 0.3))
        empty[0].set_fill(BG, opacity=1.0)
        self.at("rest of the plane")
        self.play(pop(empty), run_time=0.5)
        self.play(LaggedStart(*[f.animate.set_fill(RED, opacity=0.65) for f in list(forb)[::6]], lag_ratio=0.02),
                  run_time=0.6)
        self.play(LaggedStart(*[f.animate.set_fill(RED, opacity=0.4) for f in list(forb)[::6]], lag_ratio=0.02),
                  run_time=0.5)
        self.finish()


# ----------------------------------------------------------------------------- s04 legacy
class S04Legacy(ProfileScene):
    def construct(self):
        self.add_inset()
        # ---- sixty years on: the plot is the first check run on every new structure
        ay = 2.5
        axis = Arrow([-2.2, ay, 0], [6.1, ay, 0], color=GREY, stroke_width=3, buff=0,
                     max_tip_length_to_length_ratio=0.04)
        d1, d2 = Dot([-1.2, ay, 0], radius=0.12, color=GOLD), Dot([4.6, ay, 0], radius=0.12, color=GOLD)
        l1 = T("1963", 30, GOLD, weight=BOLD).next_to(d1, UP, buff=0.2).shift(RIGHT * 0.35)
        l2 = T("sixty years on", 30, GOLD, weight=BOLD).next_to(d2, UP, buff=0.2).shift(LEFT * 0.6)
        self.add(axis, d1, l1)
        self.at("60 years")
        self.play(FadeIn(d2, scale=2), FadeIn(l2, shift=UP * 0.1), run_time=0.6)

        C, H = np.array([3.0, -0.55, 0.0]), 1.4
        frame, forb, allow, pos = make_plane(C, H)
        for f in forb:
            f.set_fill(RED, opacity=0.4).set_stroke(RED, opacity=0.5, width=0.6)
        for a in allow:
            a.set_fill(TEAL, opacity=0.6).set_stroke(TEAL, opacity=0.9, width=1.0)
        mini = VGroup(frame, forb, allow)
        plot_lab = T("his plot", 30, TEAL).move_to([C[0], C[1] + H + 0.4, 0])
        self.at("his plot")
        self.play(FadeIn(mini, scale=0.9), FadeIn(plot_lab, shift=UP * 0.1), run_time=0.7)
        first = T("first sanity check", 30, GREEN, weight=BOLD).move_to(plot_lab)
        self.at("first sanity check")
        self.play(Transform(plot_lab, first), frame.animate.set_stroke(GREEN, width=4), run_time=0.6)

        rows = [0.4, -0.55, -1.5]
        chips = [lab("new structure", YELLOW, 24).move_to([-0.7, y, 0]) for y in rows]
        ticks = [check([5.45, y, 0]) for y in rows]
        self.at("every new protein")
        self.play(LaggedStart(*[pop(c) for c in chips], lag_ratio=0.12), run_time=0.6)
        anims = []
        for c, t, y in zip(chips, ticks, rows):
            anims.append(Succession(
                c.animate(run_time=0.45).move_to([C[0] - H - 0.9, y, 0]).set_opacity(0.0),
                Flash(np.array([C[0] + H, y, 0.0]), color=GREEN, flash_radius=0.35, line_length=0.12, run_time=0.3),
                FadeIn(t, scale=1.5, run_time=0.25),
            ))
        self.play(LaggedStart(*anims, lag_ratio=0.4), run_time=1.7)

        # ---- the Nobel Committee never called; the prizes passed him by
        self.at("Nobel", lead=0.9)
        self.play(*[FadeOut(m) for m in [axis, d1, l1, d2, l2, mini, plot_lab, *ticks]], run_time=0.5)
        nob = lab("Nobel Committee", PLACE, 30).move_to([0.3, 1.9, 0])
        him = lab(NAME, GOLD, 30).move_to([4.2, 0.2, 0])
        self.at("Nobel committee")
        self.play(pop(nob), pop(him), run_time=0.55)
        call = DashedLine(nob.get_right() + RIGHT * 0.15, [him.get_center()[0] - 0.4, him.get_top()[1] + 0.35, 0],
                          color=RED, stroke_width=4, dash_length=0.14)
        no = cross(call.get_center(), 0.24)
        never = T("never called", 30, RED, weight=BOLD).next_to(nob, DOWN, buff=0.45).align_to(nob, LEFT).shift(
            LEFT * 0.1)
        self.at("never called")
        self.play(Create(call), run_time=0.4)
        self.play(FadeIn(no, scale=1.5), FadeIn(never, shift=UP * 0.1), run_time=0.4)

        prize = lab("prizes in his field", GOLD, 30).move_to([0.3, -1.4, 0])
        self.at("prizes that touched")
        self.play(pop(prize), run_time=0.5)
        bypass = Arrow(prize.get_right() + RIGHT * 0.15, [6.2, -1.4, 0], color=GOLD, stroke_width=5, buff=0,
                       max_tip_length_to_length_ratio=0.15)
        passed = T("passed him by", 28, GOLD).next_to(bypass, DOWN, buff=0.22).align_to(bypass, RIGHT)
        self.at("passed him by")
        self.play(GrowArrow(bypass), FadeIn(passed, shift=UP * 0.1), run_time=0.8)

        # ---- he died in Chennai in 2001, after Parkinson's disease and the loss of his wife of 53 years
        self.at("He died", lead=0.7)
        self.play(*[FadeOut(m) for m in [nob, him, call, no, never, prize, bypass, passed]], run_time=0.5)
        ay2 = 2.2
        axis2 = Arrow([-2.2, ay2, 0], [6.1, ay2, 0], color=GREY, stroke_width=3, buff=0,
                      max_tip_length_to_length_ratio=0.04)
        dd = Dot([4.6, ay2, 0], radius=0.12, color=GOLD)
        died = T("died", 30, GOLD, weight=BOLD).next_to(dd, UP, buff=0.2).shift(LEFT * 0.75)
        self.at("He died")
        self.play(Create(axis2), FadeIn(dd, scale=2), FadeIn(died, shift=UP * 0.1), run_time=0.6)
        chennai = lab("Chennai", PLACE, 30).move_to([4.6, 0.85, 0])
        self.at("Chennai")
        self.play(pop(chennai), run_time=0.45)
        yr = T("2001", 34, GOLD, weight=BOLD).next_to(dd, UP, buff=0.2).shift(RIGHT * 0.5)
        self.at("2001")
        self.play(FadeIn(yr, shift=UP * 0.1), run_time=0.4)
        wire = Line(dd.get_bottom() + DOWN * 0.05, chennai.get_top(), color=PLACE, stroke_width=3)
        self.add(wire)

        park = lab("Parkinson's disease", RED, 28).move_to([-0.05, -0.5, 0])
        loss = lab("loss of his wife", RED, 28).move_to([4.5, -0.5, 0])
        self.at("Parkinson's disease")
        self.play(pop(park), run_time=0.5)
        self.at("loss of his wife")
        self.play(pop(loss), run_time=0.5)
        bar_bg = Rectangle(width=8.0, height=0.7, stroke_width=0, fill_color=GOLD, fill_opacity=0.0)
        bar_bg.move_to([PANEL_C, -2.1, 0])
        bar = Rectangle(width=0.05, height=0.7, stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to(
            [PANEL_C - 4.0 + 0.025, -2.1, 0])
        wife = T("wife of 53 years", 30, BG, weight=BOLD).move_to([PANEL_C, -2.1, 0])
        self.at("53 years", lead=0.9)
        self.play(bar.animate.stretch_to_fit_width(8.0, about_edge=LEFT), FadeIn(wife), run_time=1.0)
        self.finish()


# ----------------------------------------------------------------------------- s05 end card
class S05End(EndCard):
    LINE = "Mapped the sterically allowed backbone angles every protein structure is validated against."

    def construct(self):
        a = T("Mapped the sterically allowed backbone angles", size=40, font=TITLE_FONT)
        b = T("every protein structure is validated against.", size=40, font=TITLE_FONT)
        line = VGroup(a, b).arrange(DOWN, buff=0.22)
        fit(line, max_w=12.0)
        sub = T("biochemistrypedia.com", size=22, color=TEAL)
        g = VGroup(line, sub).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(FadeIn(line, shift=UP * 0.15), run_time=self.beat(0.3))
        self.play(FadeIn(sub), run_time=self.beat(0.15))
        self.finish()
